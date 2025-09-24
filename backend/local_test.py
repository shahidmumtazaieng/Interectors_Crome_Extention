"""
Simple test script for local API testing
"""

import requests
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")

def test_summarize():
    """Test the summarize endpoint"""
    print("\nTesting summarize endpoint...")
    try:
        response = requests.post(
            f"{BASE_URL}/summarize",
            json={"url": "https://httpbin.org/html"}
        )
        print(f"Summarize result: {response.json()}")
    except Exception as e:
        print(f"Summarize test failed: {e}")

def test_qa():
    """Test the QA endpoint"""
    print("\nTesting QA endpoint...")
    try:
        response = requests.post(
            f"{BASE_URL}/qa",
            json={
                "url": "https://httpbin.org/html",
                "question": "What is this page about?"
            }
        )
        print(f"QA result: {response.json()}")
    except Exception as e:
        print(f"QA test failed: {e}")

if __name__ == "__main__":
    print("Testing Interectors API locally...")
    print("=" * 40)
    
    test_health()
    test_summarize()
    test_qa()
    
    print("\nLocal testing completed!")