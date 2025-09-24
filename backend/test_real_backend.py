"""
Test script to verify the backend is working correctly with the real AI model
"""

import requests
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_backend():
    """Test the backend API endpoints"""
    base_url = "http://localhost:8000"
    
    print("Testing Interectors Backend with Real AI Model")
    print("=" * 50)
    
    # Test health endpoint
    try:
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test QA endpoint with a real example
    try:
        print("\n2. Testing QA endpoint with real example...")
        response = requests.post(
            f"{base_url}/qa",
            json={
                "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
                "question": "What is artificial intelligence?"
            }
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Answer: {data['answer'][:200]}...")
            print(f"   Probability: {data['probability']}")
            print(f"   Features: {data['features']}")
        else:
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test summarize endpoint
    try:
        print("\n3. Testing summarize endpoint...")
        response = requests.post(
            f"{base_url}/summarize",
            json={"url": "https://en.wikipedia.org/wiki/Machine_learning"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Summary: {data['summary'][:200]}...")
        else:
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    # Check if API key is set
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("WARNING: GOOGLE_API_KEY not found in environment variables")
        print("Please set your Google API key in the .env file")
    else:
        print(f"Google API Key found (length: {len(api_key)})")
    
    test_backend()