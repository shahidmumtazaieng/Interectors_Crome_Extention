"""
Lightweight version of the Interectors backend API for Vercel deployment
This version minimizes dependencies to stay under the 250MB limit
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import asyncio
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware for Chrome extension communication
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://*", "*"],
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

# Initialize Google Generative AI
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

genai.configure(api_key=api_key)

# Use a lighter model
model = genai.GenerativeModel('gemini-2.5-flash')

def extract_text_from_html(html_content):
    """Extract text content from HTML using BeautifulSoup"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get text and clean it up
    text = soup.get_text()
    
    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    
    # Drop blank lines
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    return text

def fetch_webpage_content(url):
    """Fetch and extract text content from a webpage"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Extract text content
        content = extract_text_from_html(response.text)
        return content[:10000]  # Limit content to 10,000 characters to stay within model limits
    except Exception as e:
        raise Exception(f"Error fetching webpage: {str(e)}")

@app.post("/summarize")
async def summarize(req: SummarizeRequest):
    try:
        # Fetch webpage content
        page_text = await asyncio.get_event_loop().run_in_executor(None, fetch_webpage_content, req.url)
        
        if not page_text:
            raise HTTPException(status_code=400, detail="Failed to extract content from the provided URL")
        
        # Generate summary using Google Generative AI directly
        prompt = f"Summarize the following web page content in under 200 words:\n\n{page_text}"
        
        response = model.generate_content(prompt)
        return {"summary": response.text}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

@app.post("/qa")
async def qa(req: QARequest):
    try:
        # Fetch webpage content
        page_text = await asyncio.get_event_loop().run_in_executor(None, fetch_webpage_content, req.url)
        
        if not page_text:
            raise HTTPException(status_code=400, detail="Failed to extract content from the provided URL")
        
        # Generate answer using Google Generative AI directly
        prompt = f"Use the following content to answer the question.\n\nContent:\n{page_text}\n\nQuestion: {req.question}\n\nAnswer:"
        
        response = model.generate_content(prompt)
        return {"answer": response.text}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Interectors Lightweight API is running"}

# Vercel requires the app to be exported as 'app'
app = app