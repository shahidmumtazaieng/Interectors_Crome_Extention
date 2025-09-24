"""
Script to verify that all required imports work correctly
"""

try:
    import os
    from dotenv import load_dotenv
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_community.document_loaders import WebBaseLoader
    from langchain.prompts import PromptTemplate
    import asyncio
    import uvicorn
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")