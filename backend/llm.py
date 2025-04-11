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
        self.online_search = DuckDuckGoSearchRun()
        self.tools = self.tool_configuration()

    def llm_configuration(self):
        self.gemini_api_key = gemini_api_key
        self.model_name = "gemini-1.5-flash"
        self.temperature = 0.7
        llm = GoogleGenerativeAI(model=self.model_name,temperature=self.temperature)
        return llm

    
    def online_search_response(self,query):
        web_search = self.online_search(query)
        prompt = f"Summarize the following to provide an accurate response and provide importance to numbers {web_search}"
        web_results  = self.llm.invoke(prompt)
        return web_results

    def tool_configuration(self):
        
        self.web_searcher = Tool(
            name = "Web Search",
            func = self.online_search_response,
            description="Search the Online Websites,Articles and News to gain higher understanding about Indain Tax System,Policies"
        )
        tools = [self.web_searcher]
        return tools


    def llm_chain(self,query:str):
        print(query)
        web_results = self.online_search_response(query)
        prompt = f'''You are an Indian Tax AI advisor and professional expert in helping indians to minize tax payments.
        Answer only relevant to the indian tax system and economics 
        use the online resources : {web_results}'''
        chains = LLMChain(
            llm  = self.llm,
            memory = self.memory,
        )
        response = chains.invoke(prompt)
        print(response)
        return response


    
    