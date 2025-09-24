# Simple Gemini API Setup

This document explains how to set up and use the simplified Gemini API implementation.

## How it works

Instead of complex Langchain chains, we're using a direct approach:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

// Simple model configuration
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

// Direct usage
response = model.invoke("Your prompt here")
result = response.content
```

## Setup Instructions

1. Get your Google API Key:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create an API key and copy it

2. Create a `.env` file in the backend directory:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   python api_server.py
   ```

## Benefits of this approach

1. **Simpler code**: No complex chain compositions
2. **Easier to understand**: Direct model usage
3. **Less dependencies**: Fewer moving parts
4. **More reliable**: Fewer points of failure
5. **Faster performance**: Using the optimized `gemini-2.5-flash` model

## Available Files

- `api_server.py` - Main API server (updated with simple approach)
- `streamlit_ui.py` - Streamlit UI (updated with simple approach)
- `simple_gemini_api.py` - Alternative simple implementation
- `requirements.txt` - Dependencies

## Testing

You can test the API with curl:

```bash
// Test summarize endpoint
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

// Test QA endpoint
curl -X POST http://localhost:8000/qa \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "question": "What is this page about?"}'
```