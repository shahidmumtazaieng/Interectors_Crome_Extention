# Project Organization Guide

To organize the Interectors project into separate backend and frontend folders, follow these steps:

## 1. Create Directory Structure

Create two new directories in your project root:
```
backend/
frontend/
```

## 2. Move Files to Backend Directory

Move the following files to the `backend/` directory:
- [api.py](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/api.py)
- [app.py](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/app.py)
- [streamlit_app.py](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/streamlit_app.py)
- [streamlit_ui.py](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/streamlit_ui.py)
- [requirements.txt](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/requirements.txt)
- [deploy_streamlit.py](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/deploy_streamlit.py)

## 3. Move Files to Frontend Directory

Move the following files to the `frontend/` directory:
- [manifest.json](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/manifest.json)
- [popup.html](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/popup.html)
- [popup.js](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/popup.js)
- [generate_icons.html](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/generate_icons.html)
- [generate_icons.py](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/generate_icons.py)
- [install_deps.bat](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/install_deps.bat)
- [icons/](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/icons) (the entire directory)

## 4. Copy Documentation

Copy the following files to both `backend/` and `frontend/` directories:
- [README.md](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/README.md)

## 5. Final Directory Structure

After organizing, your project structure should look like this:

```
crome_extention/
├── backend/
│   ├── api.py
│   ├── app.py
│   ├── streamlit_app.py
│   ├── streamlit_ui.py
│   ├── requirements.txt
│   ├── deploy_streamlit.py
│   └── README.md
├── frontend/
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   ├── generate_icons.html
│   ├── generate_icons.py
│   ├── install_deps.bat
│   ├── icons/
│   │   ├── icon16.png
│   │   ├── icon48.png
│   │   └── icon128.png
│   └── README.md
└── README.md (original)
```

## 6. Additional Configuration

### Backend Deployment
When deploying the backend to Streamlit:
1. Push only the contents of the `backend/` directory to your repository
2. Set the main file to `streamlit_app.py`

### Frontend Deployment
When packaging the Chrome extension:
1. Package only the contents of the `frontend/` directory
2. Ensure all file references in [manifest.json](file:///e:/FastAPi/Langchain/models/1LLM/crome%20extention/manifest.json) are correct

This organization makes it clear which components belong to the backend (Streamlit server) and which belong to the frontend (Chrome extension).