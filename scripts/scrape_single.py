import cloudscraper
from bs4 import BeautifulSoup
import os
import re
import time
import html
import argparse

def sanitize_filename(filename):
    """Remove invalid characters from filenames"""
    return re.sub(r'[<>:"/\\|?*]', '', filename).strip()

def get_artist_folder(artist_name):
    """Determine folder name based on artist's first character"""
    if not artist_name:
        return "Unknown"
    
    first_char = artist_name[0].upper()
    
    if first_char.isalpha():
        return first_char
    elif first_char.isdigit():
        return "0-9"
    else:
        return "Other"

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

def extract_metadata(table):
    """Extract all required metadata from the table"""
    metadata = {
        'title': 'Unknown Title',
        'artist': 'Unknown Artist',
        'genre': 'Unknown Genre',
        'difficulty': 'Unknown Difficulty',
        'harmonica': 'Unknown Harmonica',
        'key': 'Unknown Key'
    }
    
    try:
        rows = table.find_all('tr')
        
        # Row 1: Song Name and Artist
        if len(rows) > 1:
            cells = rows[1].find_all('td')
            if len(cells) > 1:
                metadata['title'] = cells[1].get_text(strip=True)
            if len(cells) > 3:
                metadata['artist'] = cells[3].get_text(strip=True)
        
        # Row 2: Difficulty
        if len(rows) > 2:
            cells = rows[2].find_all('td')
            if len(cells) > 3:
                metadata['difficulty'] = cells[3].get_text(strip=True)
        
        # Row 3: Key and Genre
        if len(rows) > 3:
            cells = rows[3].find_all('td')
            if len(cells) > 1:
                metadata['key'] = cells[1].get_text(strip=True)
            if len(cells) > 3:
                metadata['genre'] = cells[3].get_text(strip=True)
        
        # Row 4: Harp Type
        if len(rows) > 4:
            cells = rows[4].find_all('td')
            if len(cells) > 1:
                metadata['harmonica'] = cells[1].get_text(strip=True)
    
    except Exception as e:
        print(f"⚠️ Error extracting metadata: {e}")
    
    return metadata

def create_metadata_table(metadata):
    """Create a new metadata table with two-column layout"""
    return f"""
<table class="metadata">
  <tr>
    <td style="vertical-align: top; width: 50%;">
      <table>
        <tr>
          <td><font color="green">Song Name:</font></td>
          <td>{html.escape(metadata['title'])}</td>
        </tr>
        <tr>
          <td><font color="green">Artist:</font></td>
          <td>{html.escape(metadata['artist'])}</td>
        </tr>
        <tr>
          <td><font color="green">Genre:</font></td>
          <td>{html.escape(metadata['genre'])}</td>
        </tr>
      </table>
    </td>
    <td style="vertical-align: top; width: 50%;">
      <table>
        <tr>
          <td><font color="green">Harp Type:</font></td>
          <td>{html.escape(metadata['harmonica'])}</td>
        </tr>
        <tr>
          <td><font color="green">Key:</font></td>
          <td>{html.escape(metadata['key'])}</td>
        </tr>
        <tr>
          <td><font color="green">Difficulty:</font></td>
          <td>{html.escape(metadata['difficulty'])}</td>
        </tr>
      </table>
    </td>
  </tr>
</table>
"""

def download_tabs(start_id, end_id, output_base_dir="harmonica_tabs", raw_dir="data/raw", debug_empty=False):
    """Download tabs for a range of song IDs"""
    # Create output directories
    os.makedirs(output_base_dir, exist_ok=True)
    os.makedirs(raw_dir, exist_ok=True)
    
    # Create CloudScraper instance
    scraper = cloudscraper.create_scraper()
    
    # Calculate total tabs to download
    total_tabs = end_id - start_id + 1
    print(f"Starting download of {total_tabs} tabs (IDs {start_id} to {end_id})")
    
    # Initialize counters
    success_count = 0
    skip_count = 0
    error_count = 0
    
    # Loop through the range of IDs
    for idx, song_id in enumerate(range(start_id, end_id + 1)):
        # Add delay to be polite to the server
        time.sleep(1)
        
        url = f"https://www.harptabs.com/song.php?ID={song_id}"
        print(f"\nProcessing ID {idx+1}/{total_tabs} ({song_id})")
        
        try:
            # Send request
            response = scraper.get(url)
            
            # Save raw HTML
            raw_path = os.path.join(raw_dir, f"{song_id}.html")
            with open(raw_path, 'w', encoding='utf-8') as raw_file:
                raw_file.write(response.text)
            
            # Check if the request was successful
            if response.status_code != 200:
                print(f"⚠️ HTTP Error {response.status_code}")
                error_count += 1
                continue
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Use the CSS selector to find the specific <center> tag
            css_selector = 'body > center:nth-child(1) > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > center:nth-child(2)'
            target_center_tag = soup.select_one(css_selector)
            
            # Check if the <center> tag was found
            if not target_center_tag:
                print(f"⚠️ Content container not found")
                error_count += 1
                continue
                
            # Find all <table> tags inside the <center> tag
            tables = target_center_tag.find_all('table')
            
            # Check if there are at least 3 tables
            if len(tables) < 3:
                print(f"⚠️ Only {len(tables)} tables found")
                error_count += 1
                continue
                
            # Extract the first table
            first_table = tables[0]
            
            # Extract all metadata
            metadata = extract_metadata(first_table)
            
            # Get content from third table
            content_text = tables[2].get_text().strip()
            
            # Check if this is an empty page with debugging
            empty, reason = is_empty_page(
                metadata['artist'], 
                metadata['title'], 
                metadata['harmonica'], 
                metadata['key'], 
                content_text, 
                debug=debug_empty
            )
            
            if empty:
                print(f"⏩ Skipping - {reason}")
                skip_count += 1
                continue
                
            # Determine artist folder
            artist_folder = get_artist_folder(metadata['artist'])
            artist_output_dir = os.path.join(output_base_dir, artist_folder)
            os.makedirs(artist_output_dir, exist_ok=True)
                
            # Create filename
            filename = f"{metadata['artist']} - {metadata['title']} - {metadata['harmonica']} - {metadata['key']}.html"
            filename = sanitize_filename(filename)
            filepath = os.path.join(artist_output_dir, filename)
            
            # Create the HTML title
            html_title = f"{metadata['title']} by {metadata['artist']}"
            
            # Create the metadata table HTML
            metadata_table_html = create_metadata_table(metadata)
            
            # Create full HTML content with improved layout
            html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(html_title)}</title>
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
  .metadata table td {{
    border: none;
    padding: 5px 10px;
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
    overflow-x: auto;
    max-width: 100%;
    box-sizing: border-box;
    word-wrap: break-word;
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
<h1 class="page-title">{html.escape(html_title)}</h1>

{metadata_table_html}

<div class="content">
{html.escape(content_text)}
</div>

</body>
</html>
"""

            # Write to file
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(html_content)
                
            print(f"✅ Saved as {artist_folder}/{filename}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Critical error - {str(e)}")
            error_count += 1
    
    # Print summary
    print("\n" + "="*50)
    print(f"Download Summary (IDs {start_id}-{end_id})")
    print(f"Total tabs processed: {total_tabs}")
    print(f"Successfully downloaded: {success_count}")
    print(f"Skipped (empty pages): {skip_count}")
    print(f"Errors encountered: {error_count}")
    print("="*50)

if __name__ == "__main__":
    # Set up command-line arguments
    parser = argparse.ArgumentParser(description='Download harmonica tabs from harptabs.com')
    parser.add_argument('start_id', type=int, help='Starting song ID')
    parser.add_argument('end_id', type=int, help='Ending song ID')
    parser.add_argument('--output', type=str, default="harmonica_tabs", 
                        help='Output directory for processed tabs (default: harmonica_tabs)')
    parser.add_argument('--raw', type=str, default="data/raw", 
                        help='Directory for raw HTML files (default: data/raw)')
    parser.add_argument('--debug', action='store_true', 
                        help='Enable debug mode for empty page detection')
    
    args = parser.parse_args()
    
    # Validate IDs
    if args.start_id < 1:
        print("Error: start_id must be at least 1")
        exit(1)
        
    if args.end_id < args.start_id:
        print("Error: end_id must be greater than or equal to start_id")
        exit(1)
    
    print(f"Starting harmonica tabs scraper (IDs {args.start_id}-{args.end_id})...")
    
    # Create directories
    os.makedirs(args.output, exist_ok=True)
    os.makedirs(args.raw, exist_ok=True)
    
    # Run the scraper
    download_tabs(
        start_id=args.start_id,
        end_id=args.end_id,
        output_base_dir=args.output,
        raw_dir=args.raw,
        debug_empty=args.debug
    )
    
    print("Scraping completed.")