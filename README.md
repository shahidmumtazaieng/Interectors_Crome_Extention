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


## License

MIT License

## Support


For issues, feature requests, or questions, please [open an issue](https://github.com/your-username/interectors/issues) on GitHub.
