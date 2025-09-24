import os
import re
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import WebBaseLoader
from langchain.prompts import PromptTemplate
import asyncio
import uvicorn
from collections import Counter
from typing import List, Dict

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware for local development
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummarizeRequest(BaseModel):
    url: str

class QARequest(BaseModel):
    url: str
    question: str

# Initialize the model
api_key = os.getenv("GOOGLE_API_KEY")
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

# Simple feature extraction functions
def extract_keywords(text):
    """Extract keywords from text"""
    # Remove punctuation and convert to lowercase
    text = re.sub(r'[^\w\s]', '', text.lower())
    # Split into words
    words = text.split()
    # Filter out common stop words and short words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
    keywords = [word for word in words if len(word) > 3 and word not in stop_words]
    return keywords

def calculate_similarity(question_keywords, answer_keywords):
    """Calculate similarity between question and answer keywords"""
    if not question_keywords or not answer_keywords:
        return 0.0
    
    # Convert to sets for intersection
    question_set = set(question_keywords)
    answer_set = set(answer_keywords)
    
    # Calculate Jaccard similarity
    intersection = question_set.intersection(answer_set)
    union = question_set.union(answer_set)
    
    if len(union) == 0:
        return 0.0
    
    similarity = len(intersection) / len(union)
    return similarity

def extract_features(content, question, answer):
    """Extract features for visualization"""
    # Extract keywords from content, question, and answer
    content_keywords = extract_keywords(content)
    question_keywords = extract_keywords(question)
    answer_keywords = extract_keywords(answer)
    
    # Calculate similarity scores
    content_question_similarity = calculate_similarity(content_keywords, question_keywords)
    content_answer_similarity = calculate_similarity(content_keywords, answer_keywords)
    question_answer_similarity = calculate_similarity(question_keywords, answer_keywords)
    
    # Count keyword frequencies
    content_keyword_freq = Counter(content_keywords)
    question_keyword_freq = Counter(question_keywords)
    answer_keyword_freq = Counter(answer_keywords)
    
    # Get top keywords
    top_content_keywords = [kw for kw, _ in content_keyword_freq.most_common(5)]
    top_question_keywords = [kw for kw, _ in question_keyword_freq.most_common(5)]
    top_answer_keywords = [kw for kw, _ in answer_keyword_freq.most_common(5)]
    
    return {
        "content_question_similarity": round(content_question_similarity, 3),
        "content_answer_similarity": round(content_answer_similarity, 3),
        "question_answer_similarity": round(question_answer_similarity, 3),
        "top_content_keywords": top_content_keywords,
        "top_question_keywords": top_question_keywords,
        "top_answer_keywords": top_answer_keywords,
        "content_length": len(content),
        "answer_length": len(answer)
    }

# Define prompt templates
summary_template = PromptTemplate.from_template(
    "Summarize the following web page content in under 200 words:\n\n{content}"
)

qa_template = PromptTemplate.from_template(
    "Use the following content to answer the question.\n\nContent:\n{content}\n\nQuestion: {question}\n\nAnswer:"
)

def load_web_page(url: str) -> str:
    """Load and extract text from a web page"""
    loader = WebBaseLoader(url)
    documents = loader.load()
    return "\n".join([doc.page_content for doc in documents])

@app.post("/summarize")
async def summarize(req: SummarizeRequest):
    try:
        # Load web page content
        page_content = load_web_page(req.url)
        
        if not page_content:
            raise HTTPException(status_code=400, detail="Failed to extract content from the provided URL")
        
        # Generate summary using prompt template
        prompt = summary_template.format(content=page_content)
        response = model.invoke(prompt)
        
        return {"summary": response.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

@app.post("/qa")
async def qa(req: QARequest):
    try:
        # Load web page content
        page_content = load_web_page(req.url)
        
        if not page_content:
            raise HTTPException(status_code=400, detail="Failed to extract content from the provided URL")
        
        # Generate answer using prompt template
        prompt = qa_template.format(content=page_content, question=req.question)
        response = model.invoke(prompt)
        
        # Extract features for visualization
        features = extract_features(page_content, req.question, response.content)
        
        return {
            "answer": response.content,
            "features": features,
            "probability": features["question_answer_similarity"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Interectors API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)