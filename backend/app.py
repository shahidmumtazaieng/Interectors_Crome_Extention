from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import uvicorn
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware for Chrome extension communication
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://*", "*"],  # Allow all origins for testing
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

# Configure the model with error handling
try:
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
except Exception as e:
    print(f"Warning: Could not initialize gemini-2.5-flash model: {e}")
    try:
        # Fallback to a known working model
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    except Exception as e2:
        print(f"Error: Could not initialize fallback model: {e2}")
        raise

# Define prompt templates
summary_template = PromptTemplate.from_template(
    "Summarize the following web page content in under 200 words:\n\n{content}"
)

qa_template = PromptTemplate.from_template(
    "Use the following content to answer the question.\n\nContent:\n{content}\n\nQuestion: {question}\n\nAnswer:"
)

def process_web_page(url: str) -> str:
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
        
        # Generate summary using prompt template
        prompt = summary_template.format(content=page_text)
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
        
        # Generate answer using prompt template
        prompt = qa_template.format(content=page_text, question=req.question)
        response = model.invoke(prompt)
        return {"answer": response.content}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Add a root endpoint for testing
@app.get("/")
async def root():
    return {"message": "Interectors API is running"}

# Vercel requires the app to be exported as 'app'
# This is for local development
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)