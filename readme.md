#  AI Tax Advisor Chatbot -Crayon AI Hackathon

An AI-powered chatbot built to provide insights into the Indian tax system. It uses Google's Gemini LLM, integrates Pinecone for memory and vector similarity, and leverages web search tools to stay updated with the latest tax-related information.

---

<img src ="Assets\AI Tax Advisor01.png">
<img src ="Assets\AI Tax Advisor02.png">


##  Tech Stack

- Frontend     - React Js               
- Backend      - Python -FastAPI                       
- LLM          - Google Gemini 1.5-Flash (LangChain)       
- Embeddings   - Google Generative AI Embeddings         
- Vector Store - Pinecone                                
- Web Search   - Tavily Search Tool                      
- Memory       - LangChain VectorStoreRetrieverMemory    

---

## Features

- **LLM Agent**: Configured using LangChain’s to Access Web Search and Retrieval in Vector Database.
- **Memory**: Vector-based memory using Pinecone to retain chat context.
- **Web Search**: Uses Tavily to enhance knowledge with real-time data.
- **Chat Interface**: Clean, minimal UI with real-time LLM responses.

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/PARTHIBAN-007/Crayon-AI
cd Crayon-AI
```
- Create a Virtual Environment
### 2.Create .env file:
```
GEMINI_API_KEY=your_google_gemini_key
PINECONE_API_KEY=your_pinecone_key
TAVILY_API_KEY=your_tavily_key
```

### 3.Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

### 4.Frontend
```bash
cd frontend
npm install
npm start
```


