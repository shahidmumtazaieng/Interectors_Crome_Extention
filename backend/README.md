# Interectors - Backend API

The backend API for the Interectors Chrome extension, providing AI-powered webpage summarization and Q&A capabilities.

## Features

- **Page Summarization**: Get concise summaries of any web page
- **Q&A Assistant**: Ask questions about web page content
- **CORS Support**: Properly configured for Chrome extension communication
- **Health Monitoring**: Built-in health check endpoint

## API Endpoints

### Summarization
- **URL**: `/summarize`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "url": "https://example.com"
  }
  ```
- **Response**:
  ```json
  {
    "summary": "Page summary here..."
  }
  ```

### Q&A
- **URL**: `/qa`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "url": "https://example.com",
    "question": "Your question here?"
  }
  ```
- **Response**:
  ```json
  {
    "answer": "Answer to your question..."
  }
  ```

### Health Check
- **URL**: `/health`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "status": "healthy"
  }
  ```

## Technologies Used

- **Python**: Core programming language
- **Flask**: Web framework for API endpoints
- **Langchain**: AI orchestration framework
- **Google Generative AI**: Gemini model for text processing
- **WebBaseLoader**: Web page content extraction

## Deployment

### Prerequisites

1. Python 3.8 or higher
2. Google Generative AI API Key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Streamlit Cloud Deployment

1. Push this code to a GitHub repository
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Create a new app and connect it to your repository
4. Set the main file path to `streamlit_app.py`
5. Add your Google API key as a secret in the "Advanced settings" section:
   ```
   GOOGLE_API_KEY=your_actual_google_api_key_here
   ```

### Alternative Deployments

You can also deploy this Flask API to other platforms:
- Heroku
- AWS Elastic Beanstalk
- Google Cloud Run
- Azure App Service

For these platforms, you would typically:
1. Use [api.py](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/backend/api.py) as your main application file
2. Set the `GOOGLE_API_KEY` environment variable
3. Configure the platform to run `python api.py`

## Environment Variables

- `GOOGLE_API_KEY`: Your Google Generative AI API key (required)
- `FLASK_ENV`: Set to "production" for production environments

## Monitoring and Maintenance

- Monitor the `/health` endpoint for uptime
- Check logs regularly for errors
- Update dependencies periodically
- Rotate API keys as needed

## Support

For issues, feature requests, or questions, please [open an issue](https://github.com/your-username/interectors/issues) on GitHub.

## License

MIT License

## Security

- All API keys should be stored as environment variables
- CORS is configured to allow only Chrome extension origins
- No user data is stored or logged

# Interectors - Chrome Extension

A professional Chrome extension that summarizes web pages and answers questions using AI.

## Features

- **Page Summarization**: Get concise summaries of any web page
- **Q&A Assistant**: Ask questions about the current page content
- **Modern UI**: Sleek, professional interface with gradient themes
- **Cloud-Hosted Backend**: Powered by Streamlit for easy deployment

## Project Structure

```
├── manifest.json          # Chrome extension configuration
├── popup.html             # Extension popup UI
├── popup.js               # Extension functionality
├── streamlit_app.py       # Main Streamlit app entry point
├── streamlit_ui.py        # Streamlit UI components
├── api.py                 # Flask API endpoints
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── icons/                 # Extension icons
    ├── icon16.png
    ├── icon48.png
    └── icon128.png
```

## Prerequisites

1. Google Generative AI API Key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))
2. Streamlit account (free at [streamlit.io](https://streamlit.io))
3. Python 3.8 or higher

## Backend Deployment (Streamlit)

### Option 1: Deploy to Streamlit Community Cloud (Recommended)

1. Fork this repository or upload the files to a new GitHub repository
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Create a new app and connect it to your repository
4. Set the main file path to `streamlit_app.py`
5. In the "Advanced settings" section, add your Google API key as a secret:
   ```
   GOOGLE_API_KEY=your_actual_google_api_key_here
   ```
6. Click "Deploy!"

### Option 2: Run Locally for Development

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your Google API key as an environment variable:
   ```bash
   # On Windows (PowerShell)
   $env:GOOGLE_API_KEY="your_actual_google_api_key_here"
   
   # On macOS/Linux
   export GOOGLE_API_KEY="your_actual_google_api_key_here"
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

4. Run the API server (in a separate terminal):
   ```bash
   python api.py
   ```

## Chrome Extension Installation

### For Development

1. Clone or download this repository
2. Open Chrome and go to `chrome://extensions/`
3. Enable "Developer mode" (toggle in top right)
4. Click "Load unpacked"
5. Select the folder containing this repository
6. The extension will appear in your toolbar

### For Production (Publishing to Chrome Web Store)

1. Update the extension version in `manifest.json`
2. Create a zip file of all extension files (excluding backend files)
3. Go to the [Chrome Developer Dashboard](https://chrome.google.com/webstore/developer/dashboard)
4. Pay the one-time developer registration fee ($5)
5. Upload your extension package
6. Fill in the required information and submit for review

## Configuration

After deploying your Streamlit app:

1. Open `popup.js`
2. Replace the `STREAMLIT_APP_URL` value with your actual Streamlit app URL:
   ```javascript
   const STREAMLIT_APP_URL = "https://your-app-name.streamlit.app";
   ```
3. Save the file

## Usage

1. Navigate to any web page
2. Click the Interectors icon in your Chrome toolbar
3. Use the "Generate Summary" button to get a summary of the page
4. Use the Q&A section to ask questions about the page content

## API Endpoints

The backend provides two main API endpoints:

### Summarization Endpoint

- **URL**: `/summarize`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "url": "https://example.com"
  }
  ```
- **Response**:
  ```json
  {
    "summary": "Page summary here..."
  }
  ```

### Q&A Endpoint

- **URL**: `/qa`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "url": "https://example.com",
    "question": "Your question here?"
  }
  ```
- **Response**:
  ```json
  {
    "answer": "Answer to your question..."
  }
  ```

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Streamlit, Flask
- **AI Models**: Google Gemini via Langchain
- **Web Scraping**: Langchain WebBaseLoader

## Troubleshooting

- **Extension not working**: Check that your Streamlit app is deployed and accessible
- **API key issues**: Ensure your Google API key is correctly configured in Streamlit secrets
- **CORS errors**: Make sure you've enabled CORS in your Streamlit app settings
- **Chrome console errors**: Check for error messages (Ctrl+Shift+J)

## Customization

You can customize the extension by modifying:

- **UI**: Edit `popup.html` and the CSS within it
- **Functionality**: Edit `popup.js`
- **Branding**: Update `manifest.json` and icons in the `icons/` folder
- **AI Prompts**: Modify the prompt templates in `api.py`

## License

MIT License

## Support

For issues, feature requests, or questions, please [open an issue](https://github.com/your-username/interectors/issues) on GitHub.