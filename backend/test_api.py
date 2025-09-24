"""
Test script to verify that the API server is working correctly
"""

import requests
import json

# Test the summarize endpoint
def test_summarize():
    # Use the actual API server URL
    url = "https://interectorscromeextention-igrjcyl4beuxpt2xof4kmq.streamlit.app/summarize"
    data = {
        "url": "https://example.com"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

# Test the QA endpoint
def test_qa():
    # Use the actual API server URL
    url = "https://interectorscromeextention-igrjcyl4beuxpt2xof4kmq.streamlit.app/qa"
    data = {
        "url": "https://example.com",
        "question": "What is this website about?"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing Summarize Endpoint:")
    test_summarize()
    
    print("\nTesting QA Endpoint:")
    test_qa()