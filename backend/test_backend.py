"""
Simple test script to verify the backend is working correctly
"""

import requests
import time

def test_backend():
    """Test the backend API endpoints"""
    base_url = "http://localhost:8000"
    
    print("Testing Interectors Backend")
    print("=" * 30)
    
    # Test health endpoint
    try:
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test root endpoint
    try:
        print("\n2. Testing root endpoint...")
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test summarize endpoint
    try:
        print("\n3. Testing summarize endpoint...")
        response = requests.post(
            f"{base_url}/summarize",
            json={"url": "https://httpbin.org/html"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Summary: {response.json()['summary'][:100]}...")
        else:
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test QA endpoint
    try:
        print("\n4. Testing QA endpoint...")
        response = requests.post(
            f"{base_url}/qa",
            json={
                "url": "https://httpbin.org/html",
                "question": "What is this page about?"
            }
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Answer: {response.json()['answer'][:100]}...")
        else:
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_backend()