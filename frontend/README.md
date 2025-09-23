# Interectors - Chrome Extension (Production Version)

A professional Chrome extension that summarizes web pages and answers questions using AI.

## Features

- **Page Summarization**: Get concise summaries of any web page
- **Q&A Assistant**: Ask questions about the current page content
- **Modern UI**: Sleek, professional interface with gradient themes
- **Cloud-Hosted Backend**: Powered by Streamlit for easy deployment

## Production Deployment

### Prerequisites

1. Google Chrome browser
2. Access to the deployed backend API

### Installation

#### From Chrome Web Store (Recommended)
1. Visit the Chrome Web Store
2. Search for "Interectors"
3. Click "Add to Chrome"

#### Manual Installation
1. Download the packaged extension (.crx file)
2. Open Chrome and go to `chrome://extensions/`
3. Enable "Developer mode"
4. Drag and drop the .crx file onto the extensions page

### Configuration

The extension is pre-configured to work with the production backend. If you need to update the API URL:

1. Go to `chrome://extensions/`
2. Find Interectors and click "Details"
3. Click "Extension options" (if available)
4. Update the API URL

## Usage

1. Navigate to any web page
2. Click the Interectors icon in your Chrome toolbar
3. Use the "Generate Summary" button to summarize the page
4. Use the Q&A section to ask questions about the page content

## Technologies Used

- **HTML5**: Structure and content
- **CSS3**: Styling and animations
- **JavaScript**: Functionality and Chrome API integration
- **Chrome Extension Manifest V3**: Modern extension architecture

## Support

For issues, feature requests, or questions, please [open an issue](https://github.com/your-username/interectors/issues) on GitHub.

## License

MIT License

## Privacy

This extension does not collect or store any personal data. All processing is done through the backend API, and only the current page URL is sent for processing when you use the features.