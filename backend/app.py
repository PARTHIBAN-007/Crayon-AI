from main import LLM


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
obj = LLM()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(data: ChatMessage):
    
    response = obj.llm_chain(data.message)
    return {"response":response }
