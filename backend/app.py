from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import uvicorn
import asyncio
import os
import traceback
from dotenv import load_dotenv

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

# Configure the model with better error handling
def initialize_model():
    """Initialize the Google Generative AI model with fallback options"""
    models_to_try = [
        "gemini-2.5-flash",
        "gemini-pro",
        "gemini-1.5-flash"
    ]
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
    
    if api_key == "your_google_api_key_here":
        raise ValueError("GOOGLE_API_KEY is still set to the placeholder value")
    
    for model_name in models_to_try:
        try:
            print(f"Attempting to initialize model: {model_name}")
            model = ChatGoogleGenerativeAI(model=model_name)
            # Test the model with a simple prompt
            test_response = model.invoke("Say 'OK' if you're working")
            if test_response.content:
                print(f"Successfully initialized model: {model_name}")
                return model, model_name
        except Exception as e:
            print(f"Failed to initialize {model_name}: {str(e)}")
            continue
    
    raise ValueError("Could not initialize any available model")

# Initialize model at startup
try:
    model, model_name = initialize_model()
    print(f"Model initialized successfully: {model_name}")
except Exception as e:
    print(f"Model initialization failed: {str(e)}")
    model = None
    model_name = "unavailable"

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
        print(f"Loading web page: {url}")
        loader = WebBaseLoader(url)
        documents = loader.load()
        content = "\n".join([doc.page_content for doc in documents])
        print(f"Successfully loaded content, length: {len(content)} characters")
        return content
    except Exception as e:
        print(f"Error loading page {url}: {str(e)}")
        raise Exception(f"Error loading page: {str(e)}")

@app.post("/summarize")
async def summarize(req: SummarizeRequest):
    if not model:
        raise HTTPException(status_code=500, detail="AI model is not available. Check GOOGLE_API_KEY configuration.")
    
    try:
        print(f"Processing summarize request for URL: {req.url}")
        
        # Process the web page
        page_text = await asyncio.get_event_loop().run_in_executor(None, process_web_page, req.url)
        
        if not page_text:
            raise HTTPException(status_code=400, detail="Failed to extract content from the provided URL")
        
        print(f"Page content length: {len(page_text)} characters")
        
        # Generate summary using prompt template
        prompt = summary_template.format(content=page_text)
        print(f"Generated prompt length: {len(prompt)} characters")
        
        response = model.invoke(prompt)
        print("Successfully generated summary")
        
        return {"summary": response.content}
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error generating summary: {str(e)}"
        print(f"Error in summarize endpoint: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_msg)

@app.post("/qa")
async def qa(req: QARequest):
    if not model:
        raise HTTPException(status_code=500, detail="AI model is not available. Check GOOGLE_API_KEY configuration.")
    
    try:
        print(f"Processing QA request for URL: {req.url}, Question: {req.question}")
        
        # Process the web page
        page_text = await asyncio.get_event_loop().run_in_executor(None, process_web_page, req.url)
        
        if not page_text:
            raise HTTPException(status_code=400, detail="Failed to extract content from the provided URL")
        
        print(f"Page content length: {len(page_text)} characters")
        
        # Generate answer using prompt template
        prompt = qa_template.format(content=page_text, question=req.question)
        print(f"Generated prompt length: {len(prompt)} characters")
        
        response = model.invoke(prompt)
        print("Successfully generated answer")
        
        return {"answer": response.content}
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error answering question: {str(e)}"
        print(f"Error in QA endpoint: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Add a root endpoint for testing
@app.get("/")
async def root():
    return {"message": "Interectors API is running", "model_status": "available" if model else "unavailable"}

# Vercel requires the app to be exported as 'app'
# This is for local development
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)