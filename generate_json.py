import os
import json
import re

TXT_PATH = "song_library.txt"
JSON_PATH = "songs.json"

def parse_txt_library():
    if not os.path.exists(TXT_PATH):
        print(f"Error: Could not find {TXT_PATH}")
        return []

    print("Parsing full song_library.txt...")
    with open(TXT_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Split the file into blocks using common songbook separators or double newlines
    # Adjust splitting logic based on how entries are separated
    blocks = re.split(r'\n\s*\n\s*\n', content)
    
    songs = []
    
    for block in blocks:
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        if not lines:
            continue
            
        # Assume first line is title
        title = lines[0]
        
        # Filter out obvious index artifacts/dividers
        if set(title) <= {'*', '-', '=', '_', ' ', '—', '.', '·'} or len(title) < 2:
            continue
        if any(term in title.upper() for term in ["MAIN INDEX", "BY ARTIST", "CONTENTS", "SONGBOOK"]):
            continue

        artist = "Unknown Artist"
        url = ""
        lyrics_start_idx = 1

        # Check if second line is an artist or a URL
        if len(lines) > 1:
            if "youtube.com" in lines[1] or "youtu.be" in lines[1]:
                url = lines[1]
                lyrics_start_idx = 2
            elif len(lines) > 2 and ("youtube.com" in lines[2] or "youtu.be" in lines[2]):
                artist = lines[1]
                url = lines[2]
                lyrics_start_idx = 3
            else:
                # If no URL, maybe second line is artist
                artist = lines[1]
                lyrics_start_idx = 2

        lyrics = lines[lyrics_start_idx:]

        songs.append({
            'title': title,
            'artist': artist,
            'youtube': url,
            'is_sing_along': "sing-along" in title.lower() or "sing along" in artist.lower(),
            'content': lyrics
        })

    # Sort alphabetically by title
    songs = sorted(songs, key=lambda x: x['title'].lower())

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=2)

    print(f"SUCCESS: Extracted and sorted {len(songs)} songs into {JSON_PATH}.")
    return songs

if __name__ == "__main__":
    parse_txt_library()