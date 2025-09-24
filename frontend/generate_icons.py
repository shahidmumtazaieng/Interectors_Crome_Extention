"""
Script to generate SVG icons from the HTML file for the Chrome extension.
This script extracts SVG elements from the HTML and saves them as individual SVG files.
"""

import re
import os

def generate_icons():
    try:
        # Read the HTML file
        with open("generate_icons.html", "r", encoding="utf-8") as file:
            html_content = file.read()
        
        # Get the icons directory
        icons_dir = "icons"
        os.makedirs(icons_dir, exist_ok=True)
        
        # Find all SVG elements with IDs using regex
        # This pattern captures the entire SVG element including all its content
        svg_pattern = r'(<svg[^>]*id="([^"]*)"[^>]*>.*?</svg>)'
        svg_matches = re.findall(svg_pattern, html_content, re.DOTALL)
        
        # Extract and save each SVG
        for svg_full_content, svg_id in svg_matches:
            if svg_id:
                # Create the SVG file content with proper XML declaration
                svg_file_content = f'<?xml version="1.0" encoding="UTF-8"?>\n{svg_full_content}'
                
                # Save the SVG file
                svg_filename = f"{icons_dir}/{svg_id}.svg"
                with open(svg_filename, "w", encoding="utf-8") as svg_file:
                    svg_file.write(svg_file_content)
                print(f"Generated {svg_filename}")
        
        print("All SVG icons generated successfully!")
        
    except Exception as e:
        print(f"Error generating icons: {e}")

if __name__ == "__main__":
    generate_icons()