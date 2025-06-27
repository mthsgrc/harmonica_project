import sqlite3
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

def extract_tab_data(html_path):
    """Extracts metadata and content from HTML file preserving formatting"""
    with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    # Extract metadata
    meta_table = soup.find('table', class_='metadata')
    data = {
        'artist': '',
        'song': '',
        'difficulty': '',
        'genre': '',
        'harp_type': '',
        'key': ''
    }
    
    if meta_table:
        for table in meta_table.find_all('table'):
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) < 2:
                    continue
                
                key = cells[0].get_text(strip=True).lower()
                value = cells[1].get_text(strip=True)
                
                if 'artist' in key:
                    data['artist'] = value
                elif 'song' in key:
                    data['song'] = value
                elif 'difficulty' in key:
                    data['difficulty'] = value
                elif 'genre' in key:
                    data['genre'] = value
                elif 'harp' in key:
                    data['harp_type'] = value
                elif 'key' in key:
                    data['key'] = value

    # Extract content with preserved formatting
    content_div = soup.find('div', class_='content')
    content = ''
    youtube_link = ''
    
    if content_div:
        # Get raw text content with all whitespace preserved
        content = content_div.get_text('\n')
        
        # Extract YouTube link before cleaning
        youtube_match = re.search(r'https?://(?:www\.)?(?:youtube\.com|youtu\.be)\S+', content)
        if youtube_match:
            youtube_link = youtube_match.group(0)
        
        # Remove YouTube links but keep other content
        content = re.sub(r'https?://\S+', '', content)
        
        # Preserve all whitespace and special characters
        # Only remove problematic non-printable characters
        content = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', content)
    
    # Fallback to filename parsing if metadata is missing
    filename = Path(html_path).stem
    parts = filename.split(' - ')
    if len(parts) >= 4:
        if not data['artist']:
            data['artist'] = parts[0]
        if not data['song']:
            data['song'] = parts[1]
        if not data['harp_type']:
            data['harp_type'] = parts[2]
        if not data['key']:
            data['key'] = parts[3]
    
    return {
        'artist': data['artist'],
        'song': data['song'],
        'difficulty': data['difficulty'],
        'genre': data['genre'],
        'harp_type': data['harp_type'],
        'key': data['key'],
        'content': content,
        'youtube_link': youtube_link,
        'file_path': str(html_path)
    }

def import_tabs(database_path, tabs_dir):
    """Processes all HTML files and imports into database"""
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    
    # Drop and recreate table to clear existing data
    c.execute('''DROP TABLE IF EXISTS tabs''')
    c.execute('''CREATE TABLE tabs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        artist TEXT NOT NULL,
        song TEXT NOT NULL,
        difficulty TEXT,
        genre TEXT,
        harp_type TEXT NOT NULL,
        key TEXT NOT NULL,
        content TEXT NOT NULL,
        youtube_link TEXT,
        file_path TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Get all HTML files
    tabs_dir = Path(tabs_dir)
    html_files = list(tabs_dir.rglob('*.html'))
    total_files = len(html_files)
    print(f"Found {total_files} HTML files")
    
    # Import each file
    for i, html_path in enumerate(html_files):
        try:
            tab_data = extract_tab_data(html_path)
            # Insert into database
            c.execute('''INSERT INTO tabs (
                artist, song, difficulty, genre, 
                harp_type, key, content, youtube_link, file_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                tab_data['artist'],
                tab_data['song'],
                tab_data['difficulty'],
                tab_data['genre'],
                tab_data['harp_type'],
                tab_data['key'],
                tab_data['content'],
                tab_data['youtube_link'],
                tab_data['file_path']
            ))
        except Exception as e:
            print(f"Error processing {html_path}: {e}")
            continue
        
        if (i+1) % 1000 == 0:
            print(f"Processed {i+1}/{total_files} files")
            conn.commit()
    
    conn.commit()
    conn.close()
    print(f"Imported {total_files} tabs")

if __name__ == '__main__':
    DATABASE = "database/harmonica_tabs.db"
    TABS_DIR = "database/harmonica_tabs"  # Adjust to your actual path
    
    # Create database directory if needed
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    
    import_tabs(DATABASE, TABS_DIR)