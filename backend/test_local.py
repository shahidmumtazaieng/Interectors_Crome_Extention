"""
Local test script to verify the backend works before deployment
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def test_local_backend():
    """Test the backend components locally"""
    print("Testing Backend Components Locally...")
    print("=" * 40)
    
    try:
        # Test dependencies
        print("1. Testing Dependencies...")
        import fastapi
        import langchain_google_genai
        import langchain_community
        from pydantic import BaseModel
        print("✅ All dependencies imported successfully")
        
        # Test API key
        print("\n2. Testing API Key...")
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("⚠️  GOOGLE_API_KEY not found in environment variables")
            print("   This is OK for local testing, but required for deployment")
        else:
            print("✅ GOOGLE_API_KEY found")
        
        # Test model initialization
        print("\n3. Testing Model Initialization...")
        from langchain_google_genai import ChatGoogleGenerativeAI
        try:
            model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
            print("✅ Model initialized successfully")
        except Exception as e:
            print(f"⚠️  Model initialization warning: {e}")
            print("   This might be OK if the API key is not set locally")
        
        # Test web loader
        print("\n4. Testing Web Loader...")
        from langchain_community.document_loaders import WebBaseLoader
        try:
            loader = WebBaseLoader("https://httpbin.org/html")
            documents = loader.load()
            if documents:
                print(f"✅ Web loader worked, loaded {len(documents)} documents")
            else:
                print("⚠️  Web loader returned no documents")
        except Exception as e:
            print(f"⚠️  Web loader warning: {e}")
            
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if test_local_backend():
        print("\n🎉 Local test completed! Check warnings above if any.")
    else:
        print("\n💥 Local test failed. Please fix the errors before deploying.")