import os
from langchain_google_genai import GoogleGenerativeAI
import google.generativeai as genai
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
from langchain_core.tools import tool
from pinecone import Pinecone, ServerlessSpec
pinecone_api_key = os.getenv("PINECONE_API_KEY")
import time
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.tools import Tool
from langchain.chains import LLMChain
from langchain.agents import initialize_agent
class LLM():
    def __init__(self):
        self.llm = self.llm_configuration()
        self.memory = ConversationBufferMemory()
        self.retriever = self.initialize_pinecone()
        self.online_search = DuckDuckGoSearchRun()
        self.tools = self.tool_configuration()

    def llm_configuration(self):
        self.gemini_api_key = gemini_api_key
        self.model_name = "gemini-1.5-flash"
        self.temperature = 0.7
        llm = GoogleGenerativeAI(model=self.model_name,temperature=self.temperature)
        return llm

    def initialize_pinecone(self):
        pc = Pinecone(api_key=pinecone_api_key)
        index_name = "indain-tax-system"
        existing_indexes = [index_info['name'] for index_info in pc.list_indexes()]
        if index_name not in existing_indexes:
            pc.create_index(
                name = index_name,
                dimension = 768 ,
                metric = "cosine",
                spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
            )
            while not pc.describe_index(index_name).status["ready"]:
                time.sleep(1)
        index = pc.Index(index_name)


        return index

    @tool
    def ChatRetriever(self,query:str)-> str:
        """Retrieve chat History"""
        retriever = self.retriever.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 1, "score_threshold": 0.5},
        )
        response = retriever.invoke(query)
    @tool
    def online_search_response(self,query:str) -> str:
        """Retrieve Data from web"""
        web_search = self.online_search(query)
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
        tools = [self.web_searcher]
        return tools


    def llm_chain(self,query:str):
        print(self.tools)
        agent = initialize_agent(
            llm = self.llm,
            memory = self.memory,
            tools = self.tools,
            agent = "zero-shot-react-description",
            max_iterations =3,
            verbose = True,
        )
        response = agent(query)
        return response


    
    