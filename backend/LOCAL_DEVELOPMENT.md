# Local Development Guide

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Google API key:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Running the Server

Start the server locally:
```bash
python app.py
```

The API will be available at `http://localhost:8000`

## Testing the API

You can test the API endpoints using the provided test script:
```bash
python local_test.py
```

Or use curl/postman to test the endpoints directly:
- `POST /summarize` - Summarize a web page
- `POST /qa` - Ask a question about a web page
- `GET /health` - Health check
- `GET /` - Root endpoint

## API Examples

### Summarize Endpoint
```json
{
  "url": "https://example.com"
}
```

### QA Endpoint
```json
{
  "url": "https://example.com",
  "question": "What is this page about?"
}
```