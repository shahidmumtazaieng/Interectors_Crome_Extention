"""
Script to generate PNG icons from SVG files for the Chrome extension.
This script uses Selenium to render SVG files and save them as PNG.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

def generate_icons():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize the driver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Get the absolute path to the generate_icons.html file
        html_file = os.path.abspath("generate_icons.html")
        file_url = f"file://{html_file}"
        
        # Load the HTML file
        driver.get(file_url)
        time.sleep(2)  # Wait for page to load
        
        # Get the icons directory
        icons_dir = "icons"
        os.makedirs(icons_dir, exist_ok=True)
        
        # Generate screenshots for each icon size
        icon_sizes = [(16, 'icon16'), (48, 'icon48'), (128, 'icon128')]
        
        for size, element_id in icon_sizes:
            # Find the canvas element
            canvas = driver.find_element("id", element_id)
            
            # Take screenshot of just the canvas
            canvas.screenshot(f"{icons_dir}/{element_id}.png")
            print(f"Generated {icons_dir}/{element_id}.png")
            
        print("All icons generated successfully!")
        
    except Exception as e:
        print(f"Error generating icons: {e}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    generate_icons()