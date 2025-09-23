"""
Script to prepare the Interectors Chrome extension for production deployment
"""

import os
import shutil
import json
from pathlib import Path

def check_production_config():
    """Check if the extension is configured for production"""
    popup_js_path = Path("frontend/popup.js")
    
    if not popup_js_path.exists():
        print("Error: frontend/popup.js not found")
        return False
    
    with open(popup_js_path, 'r') as f:
        content = f.read()
    
    if 'IS_LOCAL_DEVELOPMENT = false' in content:
        print("✓ Extension is configured for production")
        return True
    else:
        print("⚠ Extension is still configured for local development")
        print("Please update frontend/popup.js:")
        print("  Set IS_LOCAL_DEVELOPMENT = false")
        print("  Update STREAMLIT_APP_URL with your production URL")
        return False

def check_icons():
    """Check if PNG icons exist for production"""
    icons_dir = Path("frontend/icons")
    required_icons = ["icon16.png", "icon48.png", "icon128.png"]
    missing_icons = []
    
    for icon in required_icons:
        if not (icons_dir / icon).exists():
            missing_icons.append(icon)
    
    if missing_icons:
        print(f"⚠ Missing PNG icons: {', '.join(missing_icons)}")
        print("Please convert the SVG icons to PNG format:")
        for icon in missing_icons:
            svg_icon = icon.replace(".png", ".svg")
            print(f"  {svg_icon} → {icon}")
        return False
    else:
        print("✓ All required PNG icons are present")
        return True

def check_manifest():
    """Check if manifest.json is properly configured"""
    manifest_path = Path("frontend/manifest.json")
    
    if not manifest_path.exists():
        print("Error: frontend/manifest.json not found")
        return False
    
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        required_keys = ["name", "version", "manifest_version", "description"]
        missing_keys = [key for key in required_keys if key not in manifest]
        
        if missing_keys:
            print(f"⚠ Missing keys in manifest.json: {', '.join(missing_keys)}")
            return False
        else:
            print(f"✓ manifest.json is properly configured")
            print(f"  Name: {manifest.get('name', 'N/A')}")
            print(f"  Version: {manifest.get('version', 'N/A')}")
            return True
            
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in manifest.json: {e}")
        return False

def create_deployment_package():
    """Create a ZIP file for Chrome Web Store deployment"""
    try:
        import zipfile
        
        # Create deployment directory
        deploy_dir = Path("deployment")
        deploy_dir.mkdir(exist_ok=True)
        
        # Create ZIP file
        zip_path = deploy_dir / "interectors_production.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all files from frontend directory
            for root, dirs, files in os.walk("frontend"):
                # Skip __pycache__ directories
                dirs[:] = [d for d in dirs if d != "__pycache__"]
                
                for file in files:
                    file_path = Path(root) / file
                    # Add file to ZIP with relative path
                    arc_path = file_path.relative_to("frontend")
                    zipf.write(file_path, arc_path)
        
        print(f"✓ Created deployment package: {zip_path}")
        print("This ZIP file can be uploaded to the Chrome Web Store")
        return True
        
    except Exception as e:
        print(f"Error creating deployment package: {e}")
        return False

def main():
    print("Interectors - Production Preparation")
    print("=" * 40)
    
    print("\nChecking production readiness...\n")
    
    # Check configuration
    config_ok = check_production_config()
    
    # Check icons
    icons_ok = check_icons()
    
    # Check manifest
    manifest_ok = check_manifest()
    
    # Overall status
    all_checks_passed = config_ok and icons_ok and manifest_ok
    
    print("\n" + "=" * 40)
    if all_checks_passed:
        print("✓ All checks passed! Ready for production deployment")
        
        # Offer to create deployment package
        choice = input("\nDo you want to create a deployment package? (y/n): ")
        if choice.lower() == 'y':
            create_deployment_package()
    else:
        print("✗ Some checks failed. Please address the issues above")
        print("\nRefer to DEPLOYMENT_GUIDE.md for detailed instructions")

if __name__ == "__main__":
    main()