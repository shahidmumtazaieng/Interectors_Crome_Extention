import os
import traceback
from dotenv import load_dotenv

# Load environment variables as early as possible
load_dotenv()

print("Starting application initialization...")

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_community.document_loaders import WebBaseLoader
    import asyncio
    import uvicorn
    
    print("All imports successful")
    
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Traceback: {traceback.format_exc()}")
    raise

# Initialize FastAPI app
app = FastAPI()

# Add comprehensive CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

# Model initialization with error handling
model = None
try:
    print("Initializing Google Generative AI model...")
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("WARNING: GOOGLE_API_KEY not found in environment variables")
    else:
        print(f"GOOGLE_API_KEY found (length: {len(api_key)})")
    
    # Use Langchain ChatGoogleGenerativeAI as requested
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)
    print("Model initialized successfully")
    
except Exception as e:
    print(f"Model initialization failed: {e}")
    print(f"Traceback: {traceback.format_exc()}")

async def process_web_page(url: str) -> str:
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
        print(f"Traceback: {traceback.format_exc()}")
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
        
        # Generate summary using simple custom prompt
        prompt = f"Summarize the following web page content in under 200 words:\n\n{page_text}"
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
        
        # Generate answer using simple custom prompt
        prompt = f"Use the following content to answer the question.\n\nContent:\n{page_text}\n\nQuestion: {req.question}\n\nAnswer:"
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
    model_status = "available" if model else "unavailable"
    return {"status": "healthy", "model_status": model_status}

@app.get("/")
async def root():
    model_status = "available" if model else "unavailable"
    return {"message": "Interectors API is running", "model_status": model_status}

# Vercel requires the app to be exported as 'app'
app = app

print("Application initialization completed successfully")
