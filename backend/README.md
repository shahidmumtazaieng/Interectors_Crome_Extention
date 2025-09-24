# Interectors Backend API

This is the backend API for the Interectors Chrome Extension, built with FastAPI and deployed on Vercel.

## Features

- Web page summarization using Google Gemini via Langchain
- Question answering based on web page content
- CORS support for Chrome Extension communication
- Production-ready deployment configuration for Vercel

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Langchain**: Framework for developing applications with LLMs
- **Google Gemini**: AI model for text processing
- **WebBaseLoader**: For loading web page content
- **Vercel**: Cloud platform for deployment

## Setup Instructions

### Prerequisites

1. Python 3.8 or higher
2. Google Gemini API key

### Local Development

1. Clone the repository
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file and add your Google API key:
   ```env
   GOOGLE_API_KEY=your_actual_google_api_key_here
   ```

6. Run the development server:
   ```bash
   python app.py
   ```

7. The API will be available at `http://localhost:8000`

## API Endpoints

- `POST /summarize` - Summarize a web page
  ```json
  {
    "url": "https://example.com"
  }
  ```

- `POST /qa` - Ask a question about a web page
  ```json
  {
    "url": "https://example.com",
    "question": "What is this page about?"
  }
  ```

- `GET /health` - Health check endpoint

## Deployment to Vercel

1. Create a GitHub repository with your code
2. Sign up/in to Vercel
3. Create a new project and import your GitHub repository
4. Configure the project:
   - Framework Preset: Other
   - Root Directory: backend
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: (leave empty)
5. Add your `GOOGLE_API_KEY` as an environment variable in Vercel project settings
6. Deploy!

## Environment Variables

- `GOOGLE_API_KEY` - Your Google Gemini API key (required)

## CORS Configuration

The API is configured to accept requests from Chrome extensions. The CORS middleware allows:
- Origins: `chrome-extension://*`
- Methods: All HTTP methods
- Headers: All headers

This enables seamless communication between the Chrome extension and the backend API.