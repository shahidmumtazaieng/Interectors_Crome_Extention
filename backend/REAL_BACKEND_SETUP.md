# Real Backend Setup Guide

## Prerequisites

1. Python 3.8 or higher
2. Google Gemini API key
3. Google Chrome browser

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your Google API key:
   ```env
   GOOGLE_API_KEY=your_actual_google_api_key_here
   ```

### Getting a Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key and paste it in your `.env` file

## Running the Application

### Start the Backend Server

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Run the server:
   ```bash
   python app.py
   ```

4. The API will be available at `http://localhost:8000`

### Test the API

You can test the API endpoints using the provided test script:
```bash
python test_real_backend.py
```

Or use curl to test the endpoints directly:

#### Test Health Endpoint
```bash
curl http://localhost:8000/health
```

#### Test QA Endpoint
```bash
curl -X POST http://localhost:8000/qa \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Artificial_intelligence", "question": "What is artificial intelligence?"}'
```

#### Test Summarize Endpoint
```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Machine_learning"}'
```

## API Endpoints

- `POST /summarize` - Summarize a web page
  ```json
  {
    "url": "https://example.com"
  }
  ```
  Response:
  ```json
  {
    "summary": "AI-generated summary of the web page"
  }
  ```

- `POST /qa` - Ask a question about a web page
  ```json
  {
    "url": "https://example.com",
    "question": "What is this page about?"
  }
  ```
  Response:
  ```json
  {
    "answer": "AI-generated answer to the question",
    "features": {
      "content_question_similarity": 0.75,
      "content_answer_similarity": 0.82,
      "question_answer_similarity": 0.857,
      "top_content_keywords": ["keyword1", "keyword2", ...],
      "top_question_keywords": ["keyword1", "keyword2", ...],
      "top_answer_keywords": ["keyword1", "keyword2", ...],
      "content_length": 1234,
      "answer_length": 567
    },
    "probability": 0.857
  }
  ```

- `GET /health` - Health check endpoint
  ```json
  {
    "status": "healthy"
  }
  ```

- `GET /` - Root endpoint
  ```json
  {
    "message": "Interectors API is running"
  }
  ```

## Troubleshooting

### Common Issues

1. **Module not found errors**: Make sure you've installed all dependencies with `pip install -r requirements.txt`

2. **API key issues**: Verify that your `GOOGLE_API_KEY` is correctly set in the `.env` file

3. **Web page loading issues**: Some websites may block automated scraping. Try with Wikipedia or other open sites.

4. **Port conflicts**: If port 8000 is already in use, you can change it in `app.py`

### Testing the Backend

Run the test script to verify everything is working:
```bash
python test_real_backend.py
```