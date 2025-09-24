# This is the main Streamlit app file that will be run when deployed to Streamlit Cloud
# It imports and runs the UI component

import os
import sys

# Check if we should run in API mode
if len(sys.argv) > 1 and sys.argv[1] == "api":
    # Set environment variable to indicate API mode
    os.environ["STREAMLIT_API_MODE"] = "1"
    # Import the API part
    import streamlit_ui
else:
    # Run in UI mode
    import streamlit_ui
