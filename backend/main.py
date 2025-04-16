import os
from langchain_google_genai import GoogleGenerativeAI ,GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.memory import VectorStoreRetrieverMemory
from langchain_core.tools import tool
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
import time
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.tools import Tool
from langchain.agents import initialize_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
tailvy_api_key = os.getenv("TAVILY_API_KEY")
os.environ["GOOGLE_API_KEY"] = gemini_api_key
os.environ["TAVILY_API_KEY"] = tailvy_api_key


class LLM():
    def __init__(self):
        self.llm = self.llm_configuration()
        self.vectorstore = self.initialize_pinecone()
        self.memory = VectorStoreRetrieverMemory(
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
            memory_key="chat_history"
        )
        self.online_search = TavilySearchResults(max_results=3)
        self.tools = self.tool_configuration()
        self.agent = initialize_agent(
                llm=self.llm,
                memory=self.memory,
                tools=self.tools,
                agent="zero-shot-react-description",
                verbose=True,
        )


    def llm_configuration(self):
        self.gemini_api_key = gemini_api_key
        self.model_name = "gemini-1.5-flash"
        self.temperature = 0.7
        llm = GoogleGenerativeAI(model=self.model_name,temperature=self.temperature)
        return llm

    def initialize_pinecone(self):
        pc = Pinecone(api_key=pinecone_api_key)
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        embedding = embeddings.embed_documents(["test"])[0]
        dimension = len(embedding)
        index_name = "tax-system-india"
        if not pc.has_index(index_name):
            pc.create_index(
                name=index_name,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            while not pc.describe_index(index_name).status["ready"]:
                time.sleep(1)
        index = pc.Index(index_name)
        vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
        return vectorstore  


    def ChatRetriever(self,query:str)-> str:
        """Retrieve chat History to more about user"""
        retriever = self.vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 5, "score_threshold": 0.5},
        )
        response = retriever.invoke(query)
        return response
    
    def online_search_response(self,query:str) -> str:
        """Retrieve Data from web"""
        web_search = self.online_search(query)
        print(web_search)
        return web_search

    def tool_configuration(self):
        self.chat_retriever = Tool(
            name = "Chat History",
            func = self.ChatRetriever,
            description = "Chat History about user and Indian AI Tax Advisor.Use this chat history to provide an accurate response"

        )
        self.web_searcher = Tool(
            name = "Web Search",
            func = self.online_search_response,
            description="Search the Online Websites,Articles and News to gain higher understanding about Indain Tax System,Policies"
        )
        tools = [self.web_searcher,self.chat_retriever]
        return tools


    def llm_chain(self,query:str):
        response = self.agent.invoke(query)
        return response