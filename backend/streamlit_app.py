# This is the main Streamlit app file that will be run when deployed to Streamlit Cloud
# It imports and runs the UI component

import os
import sys

# Check if we should run in API mode
# Set the STREAMLIT_API_MODE environment variable to "1" to run in API mode
if os.environ.get("STREAMLIT_API_MODE") == "1":
    # Import and run the API part
    from streamlit_ui import app
    import streamlit as st
    
    # This is needed for Streamlit to recognize this as a valid Streamlit app
    st.write("Starting API server...")
    
    # Run the Flask app directly
    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 8000))
        app.run(host='0.0.0.0', port=port, debug=False)
else:
    # Run in UI mode
    import streamlit_ui