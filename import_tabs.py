import sqlite3
import os
import re
from bs4 import BeautifulSoup
from pathlib import Path

def extract_tab_data(html_path):
    """Extracts metadata and content from HTML file"""
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
    # Extract metadata
    meta_table = soup.find('table', class_='metadata')
    if not meta_table:
        return None
        
    data = {
        'artist': '',
        'song': '',
        'difficulty': '',
        'genre': '',
        'harp_type': '',
        'key': ''
    }
    
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

    # Extract content
    content_div = soup.find('div', class_='content')
    content = content_div.get_text('\n').strip() if content_div else ''
    
    # Extract YouTube link
    youtube_link = ''
    youtube_match = re.search(r'https?://(?:www\.)?(?:youtube\.com|youtu\.be)\S+', content)
    if youtube_match:
        youtube_link = youtube_match.group(0)

    # Clean content
    content = re.sub(r'https?://\S+', '', content)  # Remove all URLs
    content = re.sub(r'[^\x00-\x7F]+', '', content)  # Remove non-ASCII characters
    content = '\n'.join(line.strip() for line in content.split('\n'))  # Normalize whitespace
    
    return {
        **data,
        'content': content,
        'youtube_link': youtube_link,
        'file_path': str(html_path)
    }

def import_tabs(database_path, tabs_dir):
    """Processes all HTML files and imports into database"""
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS tabs (
        id INTEGER PRIMARY KEY,
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
    
    html_files = list(Path(tabs_dir).rglob('*.html'))
    total_files = len(html_files)
    
    for i, html_path in enumerate(html_files):
        tab_data = extract_tab_data(html_path)
        if not tab_data:
            print(f"Skipped {html_path} (invalid format)")
            continue
            
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
        
        if (i + 1) % 1000 == 0:
            print(f"Processed {i+1}/{total_files} files...")
            conn.commit()
    
    conn.commit()
    conn.close()
    print(f"Successfully imported {total_files} tabs")

if __name__ == "__main__":
    DATABASE = "harmonica_tabs.db"
    TABS_DIR = "harmonica_tabs"
    
    import_tabs(DATABASE, TABS_DIR)