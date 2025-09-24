from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
import uvicorn
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# Add comprehensive CORS middleware for Chrome extension communication
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for maximum compatibility
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

class SummarizeRequest(BaseModel):
    url: str

class QARequest(BaseModel):
    url: str
    question: str

# Use Langchain ChatGoogleGenerativeAI model as requested
load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

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
        
        if not page_text:
            raise HTTPException(status_code=400, detail="Failed to extract content from the provided URL")
        
        # Generate summary using simple custom prompt
        prompt = f"Summarize the following web page content in under 200 words:\n\n{page_text}"
        response = model.invoke(prompt)
        return {"summary": response.content}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

@app.post("/qa")
async def qa(req: QARequest):
    try:
        # Process the web page
        page_text = await asyncio.get_event_loop().run_in_executor(None, process_web_page, req.url)
        
        if not page_text:
            raise HTTPException(status_code=400, detail="Failed to extract content from the provided URL")
        
        # Generate answer using simple custom prompt
        prompt = f"Use the following content to answer the question.\n\nContent:\n{page_text}\n\nQuestion: {req.question}\n\nAnswer:"
        response = model.invoke(prompt)
        return {"answer": response.content}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Interectors API is running"}

# Vercel requires the app to be exported as 'app'
# This is for local development
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)