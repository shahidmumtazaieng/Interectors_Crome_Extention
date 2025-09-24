"""
Main entry point for the Interectors FastAPI Server
This is the primary file for deploying to Streamlit Cloud or any other hosting platform.
"""

from app import app

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get port from environment variable or default to 8000
    port = int(os.environ.get('PORT', 8000))
    
    # Run the FastAPI app with Uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=port, log_level="info")