# Interectors - Chrome Extension

A professional Chrome extension that summarizes web pages and answers questions using AI.

## Features

- **Page Summarization**: Get concise summaries of any web page
- **Q&A Assistant**: Ask questions about the current page content
- **Modern UI**: Sleek, professional interface with gradient themes
- **Cloud-Hosted Backend**: Powered by Streamlit for easy deployment

## Project Structure

```
├── backend/               # Backend API and Streamlit interface
│   ├── api.py             # Flask API endpoints
│   ├── streamlit_app.py   # Streamlit app entry point
│   ├── streamlit_ui.py    # Streamlit UI components
│   ├── requirements.txt   # Python dependencies
│   └── README.md          # Backend documentation
├── frontend/              # Chrome extension files
│   ├── manifest.json      # Extension configuration
│   ├── popup.html         # Extension popup UI
│   ├── popup.js           # Extension functionality
│   ├── icons/             # Extension icons
│   └── README.md          # Frontend documentation
├── DEPLOYMENT_GUIDE.md    # Production deployment instructions
├── prepare_production.bat # Windows script for production preparation
└── README.md              # This file
```

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Streamlit, Flask
- **AI Models**: Google Gemini via Langchain
- **Web Scraping**: Langchain WebBaseLoader

## Production Deployment

### Backend (Streamlit Cloud)

1. Push the contents of the `backend/` directory to a GitHub repository
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Create a new app and connect it to your repository
4. Set the main file path to `streamlit_app.py`
5. Add your Google API key as a secret in Streamlit settings

### Frontend (Chrome Web Store)

1. Run the production preparation script:
   - On Windows: Double-click [prepare_production.bat](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/prepare_production.bat)
   - On macOS/Linux: Run `python prepare_production.py`

2. Upload the generated package to the Chrome Web Store Developer Dashboard

## Local Development

For local development instructions, see [LOCAL_DEVELOPMENT.md](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/LOCAL_DEVELOPMENT.md)

## Documentation

- [Backend README](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/backend/README.md) - API documentation
- [Frontend README](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/frontend/README.md) - Extension usage
- [DEPLOYMENT_GUIDE.md](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/DEPLOYMENT_GUIDE.md) - Production deployment instructions
- [LOCAL_DEVELOPMENT.md](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/LOCAL_DEVELOPMENT.md) - Local development setup

## License

MIT License

## Support

For issues, feature requests, or questions, please [open an issue](https://github.com/your-username/interectors/issues) on GitHub.