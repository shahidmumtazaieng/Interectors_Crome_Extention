"""
Deployment script for Streamlit API
This script runs the Flask API server directly
"""

import os
import sys

# Import the Flask app from streamlit_ui
from streamlit_ui import app
import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)