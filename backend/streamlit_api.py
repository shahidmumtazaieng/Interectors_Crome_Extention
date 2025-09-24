"""
Streamlit API for Interectors Chrome Extension
This is a Streamlit app that runs in API mode only, designed for deployment to Streamlit Cloud.
"""

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
from dotenv import load_dotenv
import json
import os
import sys

# Load environment variables
load_dotenv()

# Check if we're running in Streamlit
if "streamlit" in sys.modules:
    # This is for local testing with Streamlit
    st.write("This app is designed to run as an API only. Please use the API endpoints.")
    st.stop()

# API mode - handle requests directly
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["chrome-extension://*", "http://localhost:*"])

# Configure the model directly
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Function to load and process web page
async def process_web_page(url: str) -> str:
    """Load and extract text from a web page"""
    try:
        loader = WebBaseLoader(url)
        documents = loader.load()
        return "\n".join([doc.page_content for doc in documents])
    except Exception as e:
        raise Exception(f"Error loading page: {str(e)}")

# Function to summarize text
def summarize_text(text: str) -> str:
    """Generate a summary of the provided text"""
    try:
        prompt = f"Summarize the following web page content in under 200 words:\n\n{text}"
        
        # Use the model directly
        response = model.invoke(prompt)
        return response.content
    except Exception as e:
        raise Exception(f"Error summarizing text: {str(e)}")

# Function to answer questions
def answer_question(text: str, question: str) -> str:
    """Answer a question based on the provided text"""
    try:
        prompt = f"Use the following content to answer the question.\n\nContent:\n{text}\n\nQuestion: {question}\n\nAnswer:"
        
        # Use the model directly
        response = model.invoke(prompt)
        return response.content
    except Exception as e:
        raise Exception(f"Error answering question: {str(e)}")

@app.route('/summarize', methods=['POST'])
def summarize_endpoint():
    """API endpoint for summarizing web pages"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        # Process the web page
        page_text = asyncio.run(process_web_page(url))
        if not page_text:
            return jsonify({"error": "Failed to load page content"}), 500
        
        # Generate summary
        summary = summarize_text(page_text)
        return jsonify({"summary": summary})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/qa', methods=['POST'])
def qa_endpoint():
    """API endpoint for answering questions about web pages"""
    try:
        data = request.get_json()
        url = data.get('url')
        question = data.get('question')
        
        if not url or not question:
            return jsonify({"error": "URL and question are required"}), 400
        
        # Process the web page
        page_text = asyncio.run(process_web_page(url))
        if not page_text:
            return jsonify({"error": "Failed to load page content"}), 500
        
        # Generate answer
        answer = answer_question(page_text, question)
        return jsonify({"answer": answer})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)