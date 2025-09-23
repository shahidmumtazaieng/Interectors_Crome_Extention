"""
Script to automatically organize the Interectors project into backend and frontend directories.
"""

import os
import shutil

def create_directories():
    """Create backend and frontend directories"""
    os.makedirs("backend", exist_ok=True)
    os.makedirs("frontend", exist_ok=True)
    print("✓ Created backend and frontend directories")

def move_backend_files():
    """Move backend files to backend directory"""
    backend_files = [
        "api.py",
        "app.py",
        "streamlit_app.py",
        "streamlit_ui.py",
        "requirements.txt",
        "deploy_streamlit.py"
    ]
    
    for file in backend_files:
        if os.path.exists(file):
            shutil.move(file, os.path.join("backend", file))
            print(f"✓ Moved {file} to backend/")
    
    # Also copy the README
    if os.path.exists("README.md"):
        shutil.copy("README.md", "backend/")
        print("✓ Copied README.md to backend/")

def move_frontend_files():
    """Move frontend files to frontend directory"""
    frontend_files = [
        "manifest.json",
        "popup.html",
        "popup.js",
        "generate_icons.html",
        "generate_icons.py",
        "install_deps.bat"
    ]
    
    for file in frontend_files:
        if os.path.exists(file):
            shutil.move(file, os.path.join("frontend", file))
            print(f"✓ Moved {file} to frontend/")
    
    # Move icons directory
    if os.path.exists("icons") and os.path.isdir("icons"):
        shutil.move("icons", os.path.join("frontend", "icons"))
        print("✓ Moved icons/ to frontend/icons/")
    
    # Also copy the README
    if os.path.exists("README.md"):
        shutil.copy("README.md", "frontend/")
        print("✓ Copied README.md to frontend/")

def main():
    print("Organizing Interectors project...")
    print("=" * 40)
    
    # Create directories
    create_directories()
    
    # Move files
    move_backend_files()
    move_frontend_files()
    
    print("=" * 40)
    print("Project organization complete!")
    print("\nNext steps:")
    print("1. For backend deployment: Push the contents of the 'backend/' directory to your repository")
    print("2. For frontend deployment: Package the contents of the 'frontend/' directory as your Chrome extension")

if __name__ == "__main__":
    main()