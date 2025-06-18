import requests
from pathlib import Path
import time

def download_tab(tab_id: int):
    url = f"https://www.harptabs.com/song.php?ID={tab_id}"
    
    # Essential headers to mimic browser behavior
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1'
    }
    
    # Use persistent session
    with requests.Session() as session:
        try:
            # First get the index page to establish session
            session.get("https://www.harptabs.com/", headers=headers, timeout=10)
            time.sleep(1)  # Be polite with delay
            
            # Now request actual tab page
            response = session.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Verify content length
            if len(response.content) < 5000:
                raise ValueError(f"Unexpected short content: {len(response.content)} bytes")
            
            # Save output
            output_path = Path(f"data/raw/{tab_id}.html")
            output_path.write_bytes(response.content)  # Use bytes to preserve encoding
            print(f"✅ Success: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Critical error for ID {tab_id}: {str(e)}")
            return False

if __name__ == "__main__":
    download_tab(30368)