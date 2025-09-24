"""
WSGI entry point for the Interectors API Server
This file can be used with WSGI servers like Gunicorn for production deployment.
"""

from api_server import app

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)