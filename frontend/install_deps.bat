@echo off
echo Installing Python dependencies for Interectors...
pip install -r requirements.txt
echo.
echo Dependencies installed successfully!
echo.
echo To run the Streamlit app locally, use:
echo streamlit run streamlit_app.py
echo.
echo To run the API server, use:
echo python api.py
echo.
pause