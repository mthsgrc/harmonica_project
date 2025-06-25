import os
import re
import unicodedata

def capitalize_filename(filename):
    """Capitalize words in filename with proper handling of ALL CAPS and apostrophes"""
    # Separate filename and extension
    name, ext = os.path.splitext(filename)
    
    # Handle hyphens with inconsistent spacing
    parts = re.split(r' \s*-\s* ', name)
    
    processed_parts = []
    for part in parts:
        # Normalize unicode and remove non-printable characters
        part = unicodedata.normalize('NFKD', part).encode('ASCII', 'ignore').decode('ASCII')
        part = re.sub(r'[^\x20-\x7E]', '_', part)  # Replace non-ASCII
        part = re.sub(r'\s+', ' ', part).strip()    # Clean whitespace
        
        # Split into words while preserving spaces
        words = re.split(r'(\s+)', part)
        new_words = []
        
        for word in words:
            # Skip processing for whitespace chunks
            if re.match(r'\s+', word):
                new_words.append(word)
                continue
                
            # Convert ALL CAPS words to lowercase
            if word.isupper() and any(c.isalpha() for c in word):
                word = word.lower()

            # Capitalize first letter
            if word:
                word = word[0].upper() + word[1:]

            # Capitalize letters after apostrophes
            apostrophe_positions = [m.start() for m in re.finditer("'", word)]
            for pos in apostrophe_positions:
                if pos + 1 < len(word):
                    # Only capitalize if next character is a letter
                    if word[pos+1].isalpha():
                        word = word[:pos+1] + word[pos+1].upper() + word[pos+2:]
            
            new_words.append(word)
        
        processed_parts.append(''.join(new_words))
    
    # Reassemble with consistent hyphen spacing
    new_name = ' - '.join(processed_parts)
    
    # Remove problematic filesystem characters
    new_name = re.sub(r'[<>:"/\\|?*]', '', new_name)
    new_name = re.sub(r'\s+', ' ', new_name).strip()
    
    return f"{new_name}{ext}"

def process_directory(root_dir):
    """Process all HTML files in directory tree"""
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.html'):
                original_path = os.path.join(root, file)
                new_filename = capitalize_filename(file)
                
                if new_filename != file:
                    new_path = os.path.join(root, new_filename)
                    try:
                        os.rename(original_path, new_path)
                        print(f"Renamed: {file} -> {new_filename}")
                    except Exception as e:
                        print(f"Error renaming {file}: {str(e)}")

if __name__ == "__main__":
    harmonica_dir = "harmonica_tabs"
    if not os.path.exists(harmonica_dir):
        print(f"Directory not found: {harmonica_dir}")
        exit(1)
        
    print(f"Processing filenames in {harmonica_dir}...")
    process_directory(harmonica_dir)
    print("Processing complete!")