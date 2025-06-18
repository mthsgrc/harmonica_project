from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def download_tab(tab_id: int):
    url = f"https://www.harptabs.com/song.php?ID={tab_id}"
    output_path = Path(f"data/raw/{tab_id}.html")
    
    with sync_playwright() as p:
        # Use Firefox for better stealth (chromium has detectable automation flags)
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.5",
                "Referer": "https://www.harptabs.com/",
                "DNT": "1"
            }
        )
        
        page = context.new_page()
        
        try:
            # Navigate to index first to establish session
            page.goto("https://www.harptabs.com/", timeout=15000)
            time.sleep(2)
            
            # Navigate to target page
            page.goto(url, timeout=20000)
            
            # Check for blocking mechanisms
            if "403 Forbidden" in page.content() or "Access Denied" in page.content():
                raise Exception("Blocking page detected")
            
            # Wait for essential content
            page.wait_for_selector("table[width='100%']", timeout=10000)
            
            # Save HTML
            content = page.content()
            output_path.write_text(content, encoding="utf-8")
            print(f"✅ Success: {output_path}")
            
        except Exception as e:
            print(f"❌ Critical error for ID {tab_id}: {str(e)}")
            return False
            
        finally:
            browser.close()
    return True

if __name__ == "__main__":
    download_tab(30368)