import cloudscraper
from bs4 import BeautifulSoup

# Create a CloudScraper instance
scraper = cloudscraper.create_scraper()

# Define the range of IDs to download
start_id = 30368  # Starting ID
end_id = 30368    # Ending ID (inclusive)

# Loop through the range of IDs
for song_id in range(start_id, end_id + 1):
    # Construct the URL for the current ID
    url = f"https://www.harptabs.com/song.php?ID={song_id}"
    
    # Send a GET request to the URL
    response = scraper.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Use the provided CSS selector to find the specific <center> tag
        css_selector = 'body > center:nth-child(1) > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > center:nth-child(2)'
        target_center_tag = soup.select_one(css_selector)
        
        # Check if the <center> tag was found
        if target_center_tag:
            # Find all <table> tags inside the <center> tag
            tables = target_center_tag.find_all('table')
            
            # Check if there are at least 3 tables
            if len(tables) >= 3:
                # Extract the first table
                first_table = tables[0]
                
                # Extract data for the file name from the specified rows and cells
                try:
                    # Find all <tr> tags inside the first table
                    rows = first_table.find_all('tr')
                    
                    # [artist_name] = from second tr, fourth td
                    if len(rows) > 1:
                        artist_name_td = rows[1].find_all('td')
                        if len(artist_name_td) > 3:
                            artist_name = artist_name_td[3].get_text(strip=True)
                        else:
                            artist_name = "Unknown Artist"
                    else:
                        artist_name = "Unknown Artist"
                    
                    # [song-name] = from second tr, second td
                    if len(rows) > 1:
                        song_name_td = rows[1].find_all('td')
                        if len(song_name_td) > 1:
                            song_name = song_name_td[1].get_text(strip=True)
                        else:
                            song_name = "Unknown Song"
                    else:
                        song_name = "Unknown Song"
                    
                    # [harmonica] = from fifth tr, second td
                    if len(rows) > 4:
                        harmonica_td = rows[4].find_all('td')
                        if len(harmonica_td) > 1:
                            harmonica = harmonica_td[1].get_text(strip=True)
                        else:
                            harmonica = "Unknown Harmonica"
                    else:
                        harmonica = "Unknown Harmonica"
                    
                    # [key] = from fourth tr, second td
                    if len(rows) > 3:
                        key_td = rows[3].find_all('td')
                        if len(key_td) > 1:
                            key = key_td[1].get_text(strip=True)
                        else:
                            key = "Unknown Key"
                    else:
                        key = "Unknown Key"
                    
                    # Create the file name
                    filename = f"{artist_name} - {song_name} - {harmonica} - {key}.html"
                    
                    # Sanitize the file name to remove invalid characters
                    filename = "".join(c if c.isalnum() or c in " -_" else "_" for c in filename)
                    
                    # Extract the second to fifth rows (index 1 to 4) from the first table
                    selected_rows = rows[1:5]
                    
                    # Combine the selected rows into a new HTML structure
                    refined_first_table = "<table><tbody>"
                    for row in selected_rows:
                        refined_first_table += row.prettify()
                    refined_first_table += "</tbody></table>"
                    
                    # Extract the third table
                    third_table = tables[2].prettify()
                    
                    # Combine the refined first table and the third table
                    filtered_content = f"{refined_first_table}\n{third_table}"
                    
                    # Write the filtered content to a file
                    with open(filename, 'w', encoding='utf-8') as file:
                        file.write(filtered_content)
                    print(f"ID {song_id}: Refined tables written to '{filename}'")
                except Exception as e:
                    print(f"ID {song_id}: Error processing the page. Details: {e}")
            else:
                print(f"ID {song_id}: The <center> tag does not contain at least 3 tables.")
        else:
            print(f"ID {song_id}: The specific <center> tag was not found using the provided CSS selector.")
    else:
        print(f"ID {song_id}: Failed to retrieve the page. Status code: {response.status_code}")