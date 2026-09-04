import os
import json
import re

TXT_PATH = "song_library.txt"
JSON_PATH = "songs.json"

def is_valid_title(title):
    clean_t = title.strip()
    if not clean_t or len(clean_t) > 60:
        return False
    if all(c in '*-_= .—·#/' for c in clean_t):
        return False
    
    upper_t = clean_t.upper()
    
    if upper_t in {"(MAIN)", "MAIN", "INDEX", "CONTENTS", "POP/ROCK"}:
        return False
    if upper_t.startswith("TIP:") or upper_t.startswith("NOTE:") or upper_t.startswith("INTRO:") or upper_t.startswith("INSTRUCTIONS:") or upper_t.startswith("B -"):
        return False
    if "BY SONG TITLE" in upper_t or "POP/ROCK" in upper_t or "GENRE" in upper_t:
        return False
    if clean_t.startswith("[") or clean_t.startswith("<"):
        return False
        
    if clean_t[0].islower():
        return False
        
    words = clean_t.split()
    chord_token = re.compile(r'^[A-G][b#]?(m|maj|min|dim|aug|sus|7|9|11|13|2|4|add)*$', re.IGNORECASE)
    chord_count = sum(1 for w in words if chord_token.match(w) or w in {'-', '—', '/', 'and', '&', ';', ','})
    if len(words) >= 2 and chord_count / len(words) >= 0.6:
        return False

    if re.search(r'\b[a-z]+,\s+[a-z]+', clean_t) or clean_t.endswith('.'):
        return False

    return True

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
            
        candidate_title = lines[0]
        
        if is_valid_title(candidate_title):
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
                    if len(lines[1]) < 40 and not lines[1].endswith('.'):
                        artist = lines[1]
                        lyrics_start_idx = 2

            lyrics = lines[lyrics_start_idx:]

            songs.append({
                'title': candidate_title,
                'artist': artist,
                'youtube': url,
                'is_sing_along': "sing-along" in candidate_title.lower() or "sing along" in artist.lower(),
                'content': lyrics
            })
        else:
            if songs:
                songs[-1]['content'].append("")
                songs[-1]['content'].extend(lines)
            else:
                songs.append({
                    'title': "Untitled / Spoken Word",
                    'artist': "Unknown Artist",
                    'youtube': "",
                    'is_sing_along': False,
                    'content': lines
                })

    songs = sorted(songs, key=lambda x: x['title'].lower())

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=2)

    print(f"SUCCESS: Cleaned, healed, and saved {len(songs)} valid songs into {JSON_PATH}.")
    return songs

if __name__ == "__main__":
    parse_txt_library()