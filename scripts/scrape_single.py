import cloudscraper
from bs4 import BeautifulSoup
import os
import re
import time

def sanitize_filename(filename):
    """Remove invalid characters from filenames"""
    return re.sub(r'[<>:"/\\|?*]', '', filename).strip()

def is_empty_page(artist, title, harmonica, key, content_text, debug=False):
    """
    Check if the page is empty with detailed debugging
    Returns tuple: (is_empty, reason)
    """
    reasons = []
    
    # Check for empty metadata
    empty_metadata = (
        artist in ['', 'Unknown Artist', 'None'] and 
        title in ['', 'Unknown Song', 'None'] and 
        harmonica in ['Unknown Harmonica', 'None'] and 
        key in ['Unknown Key', 'None']
    )
    
    if empty_metadata:
        reasons.append("Empty metadata")
    
    # Check for minimal tab content
    content_too_short = len(content_text.strip()) < 20
    
    if content_too_short:
        reasons.append(f"Content too short ({len(content_text.strip())} chars)")
    
    # Final decision based only on metadata and content length
    is_empty = empty_metadata or content_too_short
    reason = " | ".join(reasons) if reasons else "Page not empty"
    
    if debug:
        print(f"Empty Page Debug - Artist: '{artist}' | Title: '{title}'")
        print(f"Harmonica: '{harmonica}' | Key: '{key}'")
        print(f"Content length: {len(content_text.strip())} chars")
        print(f"Content snippet: {content_text[:100]}...")
        print(f"Empty? {is_empty} - Reason: {reason}")
        print("-" * 50)
    
    return is_empty, reason

def download_tabs(start_id, end_id, output_dir="harmonica_tabs", debug_empty=False):
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Create CloudScraper instance
    scraper = cloudscraper.create_scraper()
    
    # Loop through the range of IDs
    for song_id in range(start_id, end_id + 1):
        # Add delay to be polite to the server
        time.sleep(1)
        
        url = f"https://www.harptabs.com/song.php?ID={song_id}"
        print(f"\nProcessing ID: {song_id}")
        
        try:
            # Send request
            response = scraper.get(url)
            
            # Check if the request was successful
            if response.status_code != 200:
                print(f"⚠️ HTTP Error {response.status_code}")
                continue
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Use the CSS selector to find the specific <center> tag
            css_selector = 'body > center:nth-child(1) > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > center:nth-child(2)'
            target_center_tag = soup.select_one(css_selector)
            
            # Check if the <center> tag was found
            if not target_center_tag:
                print(f"⚠️ Content container not found")
                continue
                
            # Find all <table> tags inside the <center> tag
            tables = target_center_tag.find_all('table')
            
            # Check if there are at least 3 tables
            if len(tables) < 3:
                print(f"⚠️ Only {len(tables)} tables found")
                continue
                
            # Extract the first table
            first_table = tables[0]
            
            # Extract metadata
            artist = "Unknown Artist"
            title = "Unknown Song"
            harmonica = "Unknown Harmonica"
            key = "Unknown Key"
            
            try:
                # Find all <tr> tags inside the first table
                rows = first_table.find_all('tr')
                
                # Extract artist name from second tr, fourth td
                if len(rows) > 1:
                    artist_td = rows[1].find_all('td')
                    if len(artist_td) > 3:
                        artist = artist_td[3].get_text(strip=True) or artist
                
                # Extract song name from second tr, second td
                if len(rows) > 1:
                    title_td = rows[1].find_all('td')
                    if len(title_td) > 1:
                        title = title_td[1].get_text(strip=True) or title
                
                # Extract harmonica type from fifth tr, second td
                if len(rows) > 4:
                    harmonica_td = rows[4].find_all('td')
                    if len(harmonica_td) > 1:
                        harmonica = harmonica_td[1].get_text(strip=True) or harmonica
                
                # Extract key from fourth tr, second td
                if len(rows) > 3:
                    key_td = rows[3].find_all('td')
                    if len(key_td) > 1:
                        key = key_td[1].get_text(strip=True) or key
            except Exception as e:
                print(f"⚠️ Error extracting metadata - {e}")
            
            # Get content from third table
            content_text = tables[2].get_text().strip()
            
            # Check if this is an empty page with debugging
            empty, reason = is_empty_page(artist, title, harmonica, key, content_text, debug=debug_empty)
            
            if empty:
                print(f"⏩ Skipping - {reason}")
                continue
                
            # Create filename
            filename = f"{artist} - {title} - {harmonica} - {key}.html"
            filename = sanitize_filename(filename)
            filepath = os.path.join(output_dir, filename)
            
            # Create the HTML title
            html_title = f"{title} by {artist}" if artist != "Unknown Artist" else title
            
            # Create full HTML content
            html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_title}</title>
<style>
  body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    color: #333;
    line-height: 1.6;
  }}
  .metadata {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 25px;
    background-color: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }}
  .metadata td {{
    padding: 10px 15px;
    border: 1px solid #e0e0e0;
  }}
  .metadata tr:nth-child(odd) {{
    background-color: #f5f5f5;
  }}
  .metadata tr:first-child {{
    background-color: #e9f7ef;
    font-weight: bold;
  }}
  .content {{
    font-family: 'Courier New', monospace;
    white-space: pre-wrap;
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    border-left: 4px solid #4CAF50;
    font-size: 16px;
    line-height: 1.4;
  }}
  .page-title {{
    text-align: center;
    margin-bottom: 25px;
    color: #2c3e50;
    padding-bottom: 10px;
    border-bottom: 2px solid #4CAF50;
  }}
</style>
</head>
<body>
<h1 class="page-title">{html_title}</h1>

<table class="metadata">
"""

            # Add metadata rows to HTML
            try:
                rows = first_table.find_all('tr')
                for i in [1, 2, 3, 4]:  # Only include relevant rows
                    if i < len(rows):
                        html_content += rows[i].prettify()
            except:
                html_content += "<tr><td>Metadata unavailable</td></tr>"

            # Complete HTML content
            html_content += f"""
</table>

<div class="content">
{content_text}
</div>

</body>
</html>
"""

            # Write to file
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(html_content)
                
            print(f"✅ Saved as {filename}")
            
        except Exception as e:
            print(f"❌ Critical error - {str(e)}")

if __name__ == "__main__":
    print("Starting harmonica tabs scraper...")
    
    # Enable debug mode for empty page detection
    DEBUG_EMPTY = True  # Set to False to disable debug output
    
    download_tabs(
        start_id=30359,
        end_id=30369,
        output_dir="harmonica_tabs",
        debug_empty=DEBUG_EMPTY
    )
    print("Scraping completed. Check 'harmonica_tabs' directory for results.")