"""
Test script to verify that the API server is working correctly
"""

import requests
import json

# Test URLs
LOCAL_API_URL = "http://localhost:8000"
STREAMLIT_API_URL = "https://interectorscromeextention-igrjcyl4beuxpt2xof4kmq.streamlit.app"

# Test data
test_url = "https://example.com"
test_question = "What is this website about?"

def test_health_endpoint(base_url):
    """Test the health endpoint"""
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check - Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Health check successful!")
            print(f"Response: {response.json()}")
        else:
            print(f"Health check failed: {response.text}")
    except Exception as e:
        print(f"Health check error: {e}")

def test_summarize_endpoint(base_url):
    """Test the summarize endpoint"""
    try:
        response = requests.post(
            f"{base_url}/summarize",
            json={"url": test_url},
            headers={"Content-Type": "application/json"}
        )
        print(f"Summarize - Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Summarize successful!")
            print(f"Summary: {response.json().get('summary', 'No summary found')[:100]}...")
        else:
            print(f"Summarize failed: {response.text}")
    except Exception as e:
        print(f"Summarize error: {e}")

def test_qa_endpoint(base_url):
    """Test the QA endpoint"""
    try:
        response = requests.post(
            f"{base_url}/qa",
            json={"url": test_url, "question": test_question},
            headers={"Content-Type": "application/json"}
        )
        print(f"QA - Status Code: {response.status_code}")
        if response.status_code == 200:
            print("QA successful!")
            print(f"Answer: {response.json().get('answer', 'No answer found')[:100]}...")
        else:
            print(f"QA failed: {response.text}")
    except Exception as e:
        print(f"QA error: {e}")

if __name__ == "__main__":
    print("Testing LOCAL API connection...")
    print("=" * 40)
    test_health_endpoint(LOCAL_API_URL)
    print()
    test_summarize_endpoint(LOCAL_API_URL)
    print()
    test_qa_endpoint(LOCAL_API_URL)
    
    print("\n" + "=" * 50)
    print("Testing STREAMLIT API connection...")
    print("=" * 40)
    test_health_endpoint(STREAMLIT_API_URL)
    print()
    test_summarize_endpoint(STREAMLIT_API_URL)
    print()
    test_qa_endpoint(STREAMLIT_API_URL)