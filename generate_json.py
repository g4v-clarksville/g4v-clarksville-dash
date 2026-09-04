import os
import json
import re

TXT_PATH = "song_library.txt"
JSON_PATH = "songs.json"

def parse_txt_library():
    if not os.path.exists(TXT_PATH):
        print(f"Error: Could not find {TXT_PATH}")
        return []

    print("Parsing and strictly filtering song_library.txt...")
    with open(TXT_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    blocks = re.split(r'\n\s*\n\s*\n', content)
    songs = []
    
    for block in blocks:
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        if not lines:
            continue
            
        title = lines[0]
        
        # Aggressive filter to drop all index artifacts, dividers, and alphabetical section headers
        is_junk = (
            set(title) <= {'*', '-', '=', '_', ' ', '—', '.', '·'} or
            len(title) < 2 or
            re.match(r'^\s*[-—]\s*[A-Z0-9#]\s*[-—]\s*$', title) or
            re.match(r'^\(?(Main|Index|Contents|Part)\)?$', title, re.IGNORECASE) or
            any(term in title.upper() for term in [
                "MAIN INDEX", "BY ARTIST", "CONTENTS", "SONGBOOK", 
                "POP/ROCK", "TITLES IN RED", "INDEX"
            ])
        )
        
        if is_junk:
            continue

        artist = "Unknown Artist"
        url = ""
        lyrics_start_idx = 1

        if len(lines) > 1:
            if "youtube.com" in lines[1] or "youtu.be" in lines[1]:
                url = lines[1]
                lyrics_start_idx = 2
            elif len(lines) > 2 and ("youtube.com" in lines[2] or "youtu.be" in lines[2]):
                artist = lines[1]
                url = lines[2]
                lyrics_start_idx = 3
            else:
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

    # Sort alphabetically by song title
    songs = sorted(songs, key=lambda x: x['title'].lower())

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=2)

    print(f"SUCCESS: Cleaned and saved {len(songs)} valid songs into {JSON_PATH}.")
    return songs

if __name__ == "__main__":
    parse_txt_library()