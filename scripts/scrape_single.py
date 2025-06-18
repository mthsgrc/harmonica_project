import requests
from pathlib import Path

def download_tab(tab_id: int):
    url = f"https://www.harptabs.com/song.php?ID={tab_id}"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        output_path = Path(f"data/raw/{tab_id}.html")
        output_path.write_text(response.text, encoding='utf-8')
        print(f"Saved: {output_path}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading ID {tab_id}: {str(e)}")

if __name__ == "__main__":
    download_tab(30368)  # Test with target ID