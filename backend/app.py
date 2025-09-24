from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
import uvicorn
import asyncio
from dotenv import load_dotenv
import json

import sys

# Load environment variables
load_dotenv()

app = FastAPI()

class SummarizeRequest(BaseModel):
    url: str

class QARequest(BaseModel):
    url: str
    question: str

# Configure the model directly
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

async def process_web_page(url: str) -> str:
    """Load and extract text from a web page"""
    try:
        loader = WebBaseLoader(url)
        documents = loader.load()
        return "\n".join([doc.page_content for doc in documents])
    except Exception as e:
        raise Exception(f"Error loading page: {str(e)}")

@app.post("/summarize")
async def summarize(req: SummarizeRequest):
    try:
        # Process the web page
        page_text = await asyncio.get_event_loop().run_in_executor(None, process_web_page, req.url)
        
        # Generate summary using direct model invocation
        prompt = f"Summarize the following web page content in under 200 words:\n\n{page_text}"
        response = model.invoke(prompt)
        return {"summary": response.content}
    except Exception as e:
        return {"error": str(e)}

@app.post("/qa")
async def qa(req: QARequest):
    try:
        # Process the web page
        page_text = await asyncio.get_event_loop().run_in_executor(None, process_web_page, req.url)
        
        # Generate answer using direct model invocation
        prompt = f"Use the following content to answer the question.\n\nContent:\n{page_text}\n\nQuestion: {req.question}\n\nAnswer:"
        response = model.invoke(prompt)
        return {"answer": response.content}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":

    uvicorn.run(app, host="https://interectorscromeextention-ia6dt2a3vdvrbrrzyx3gbn.streamlit.app/", port=8001)

