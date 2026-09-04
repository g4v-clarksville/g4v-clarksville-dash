import os
import json
import re

TXT_PATH = "song_library.txt"
JSON_PATH = "songs.json"

def is_garbage_title(title):
    clean_t = title.strip()
    if not clean_t or len(clean_t) < 2:
        return True
    if all(c in '*-_= .—·#/' for c in clean_t):
        return True
    
    upper_t = clean_t.upper()
    
    # Standard header and keyword exclusions
    if upper_t in {"(MAIN)", "MAIN", "INDEX", "CONTENTS", "POP/ROCK"}:
        return True
    if upper_t.startswith("TIP:") or upper_t.startswith("NOTE:") or upper_t.startswith("INTRO:") or upper_t.startswith("INSTRUCTIONS:"):
        return True
    if "BY SONG TITLE" in upper_t or "POP/ROCK" in upper_t or "GENRE" in upper_t:
        return True
    if clean_t.startswith("[") or clean_t.startswith("<"):
        return True
        
    # Catch lines that are just short musical notes or chord snippets separated by dashes/spaces (e.g. "b – c", "d C A A7")
    if re.match(r'^[a-gA-G0-9\s\-\—\/\,\;\(\)\|]+$', clean_t) and len(clean_t.split()) <= 6:
        return True

    # Check if title has chord-heavy formatting or numbers/symbols typical of tablature/instructions
    words = clean_t.split()
    chord_token = re.compile(r'^[A-G][b#]?(m|maj|min|dim|aug|sus|7|9|11|13|2|4|add)*$', re.IGNORECASE)
    chord_count = sum(1 for w in words if chord_token.match(w) or w in {'-', '—', '/', 'and', '&', ';', ','})
    if len(words) >= 2 and chord_count / len(words) >= 0.6:
        return True

    if re.match(r'^[-—\s]*[A-Z0-9][-—\s]*$', clean_t, re.IGNORECASE) and len(clean_t) <= 7:
        return True
    if re.match(r'^\(.*\)$', clean_t):
        return True
        
    return False

def parse_txt_library():
    if not os.path.exists(TXT_PATH):
        print(f"Error: Could not find {TXT_PATH}")
        return []

    with open(TXT_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    blocks = re.split(r'\n\s*\n\s*\n', content)
    songs = []
    
    for block in blocks:
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        if not lines:
            continue
            
        title = lines[0]
        if is_garbage_title(title):
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

    songs = sorted(songs, key=lambda x: x['title'].lower())

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=2)

    print(f"SUCCESS: Cleaned and saved {len(songs)} valid songs into {JSON_PATH}.")
    return songs

if __name__ == "__main__":
    parse_txt_library()