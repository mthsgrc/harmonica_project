import cloudscraper
from pathlib import Path
import time
import random
import re

def download_tab(tab_id: int):
    url = f"https://www.harptabs.com/song.php?ID={tab_id}"
    output_path = Path(f"data/raw/{tab_id}.html")
    
    # Create cloudscraper instance
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'firefox',
            'platform': 'linux',
            'desktop': True
        }
    )
    
    try:
        # First request to establish session
        scraper.get("https://www.harptabs.com/", timeout=15)
        time.sleep(random.uniform(1.0, 3.0))  # Random delay
        
        # Target request
        response = scraper.get(url, timeout=30)
        
        # Validate response
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.reason}")
            
        # Check for blocking patterns
        if any(pattern in response.text for pattern in ['Forbidden', 'Access Denied', 'Cloudflare']):
            raise Exception("Blocking mechanism detected in content")
            
        # Validate content structure
        if not re.search(r'<table.*?>.*?<td class="heading".*?>', response.text, re.DOTALL):
            raise Exception("Essential table structure not found")
            
        # Save content
        output_path.write_text(response.text, encoding='utf-8')
        print(f"✅ Success: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error for ID {tab_id}: {str(e)}")
        # Save partial content for debugging
        if 'response' in locals():
            output_path.write_text(response.text, encoding='utf-8')
            print(f"⚠️ Saved partial content to {output_path}")
        return False

if __name__ == "__main__":
    download_tab(30368)