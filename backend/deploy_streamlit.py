"""
Deployment helper script for Streamlit app.
This script provides instructions and helper functions for deploying to Streamlit Cloud.
"""

import os
import subprocess
import sys

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import langchain
        import flask
        print("✓ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def test_api_key():
    """Check if Google API key is set"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print("✓ Google API key is set")
        return True
    else:
        print("⚠ Google API key is not set")
        print("Please set the GOOGLE_API_KEY environment variable")
        return False

def run_local_test():
    """Run local test of the Streamlit app"""
    print("Starting local Streamlit test...")
    try:
        subprocess.run(["streamlit", "run", "streamlit_app.py"], check=True)
    except subprocess.CalledProcessError:
        print("Error running Streamlit app")
    except FileNotFoundError:
        print("Streamlit not found. Please install it with: pip install streamlit")

def main():
    print("Interectors - Streamlit Deployment Helper")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check API key
    test_api_key()
    
    print("\nDeployment Instructions:")
    print("1. Push your code to a GitHub repository")
    print("2. Go to https://streamlit.io/cloud")
    print("3. Create a new app and connect to your repository")
    print("4. Set the main file path to 'streamlit_app.py'")
    print("5. Add your Google API key as a secret:")
    print("   GOOGLE_API_KEY=your_actual_api_key_here")
    print("6. Deploy the app")
    
    # Ask user if they want to run local test
    choice = input("\nDo you want to run a local test? (y/n): ")
    if choice.lower() == 'y':
        run_local_test()

if __name__ == "__main__":
    main()
"""
Streamlit deployment configuration for FastAPI backend
This script helps configure the Streamlit Cloud deployment for the FastAPI backend.
"""

import os
import sys

def main():
    print("Streamlit Cloud Deployment Configuration for FastAPI Backend")
    print("=" * 60)
    print()
    print("To deploy the FastAPI backend to Streamlit Cloud:")
    print()
    print("1. Push the contents of the 'backend/' directory to a GitHub repository")
    print("2. Go to https://streamlit.io/cloud")
    print("3. Create a new app and connect it to your repository")
    print("4. Set the main file path to 'main.py'")
    print("5. Add these environment variables in the Streamlit Cloud settings:")
    print("   - Key: GOOGLE_API_KEY")
    print("   - Value: your_actual_api_key_here")
    print()
    print("The FastAPI server will automatically start on the port provided by Streamlit Cloud.")
    print("Your API endpoints will be available at:")
    print("  - POST /summarize")
    print("  - POST /qa")
    print("  - GET /health")

if __name__ == "__main__":
    main()
