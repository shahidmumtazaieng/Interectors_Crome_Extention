"""
Test script for the Interectors backend API
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration
BASE_URL = "http://localhost:8000"  # Change this to your deployed URL for testing deployed version

def test_health():
    """Test the health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:", response.json())

def test_summarize():
    """Test the summarize endpoint"""
    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    payload = {"url": url}
    
    response = requests.post(f"{BASE_URL}/summarize", json=payload)
    print("\nSummarize Response:")
    print(response.json())

def test_qa():
    """Test the QA endpoint"""
    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    payload = {
        "url": url,
        "question": "What is artificial intelligence?"
    }
    
    response = requests.post(f"{BASE_URL}/qa", json=payload)
    print("\nQA Response:")
    print(response.json())

if __name__ == "__main__":
    print("Testing Interectors Backend API")
    print("=" * 40)
    
    try:
        test_health()
        test_summarize()
        test_qa()
    except Exception as e:
        print(f"Error during testing: {e}")