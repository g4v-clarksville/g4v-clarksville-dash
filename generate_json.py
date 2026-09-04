import os
import json
import re

TXT_PATH = "song_library.txt"
JSON_PATH = "songs.json"

def parse_txt_library():
    if not os.path.exists(TXT_PATH):
        print(f"Error: Could not find {TXT_PATH}")
        return []

    print("Parsing song_library.txt line-by-line...")
    with open(TXT_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [line.strip() for line in f.readlines()]

    songs = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines or absolute junk artifacts
        if not line:
            i += 1
            continue
            
        is_junk = (
            set(line) <= {'*', '-', '=', '_', ' ', '—', '.', '·'} or
            len(line) < 2 or
            line.startswith('(') or
            line.endswith(')') or
            re.match(r'^\s*[-—]\s*[A-Z0-9#]\s*[-—]\s*$', line) or
            any(term in line.upper() for term in [
                "MAIN INDEX", "BY ARTIST", "CONTENTS", "SONGBOOK", 
                "POP/ROCK", "TITLES IN RED", "INDEX"
            ])
        )
        
        if is_junk:
            i += 1
            continue

        # Look ahead to see if this line functions as a song title (followed by artist or url)
        if i + 1 < len(lines):
            next_line = lines[i + 1]
            
            # Check if current line is a valid title and next line is artist or YouTube link
            if next_line and not set(next_line) <= {'*', '-', '=', '_', ' ', '—', '.', '·'}:
                title = line
                artist = "Unknown Artist"
                url = ""
                content = []
                
                i += 1
                # Check if next line is a YouTube URL or Artist
                if "youtube.com" in next_line or "youtu.be" in next_line:
                    url = next_line
                    i += 1
                elif i + 1 < len(lines) and ("youtube.com" in lines[i+1] or "youtu.be" in lines[i+1]):
                    artist = next_line
                    i += 1
                    url = lines[i]
                    i += 1
                else:
                    artist = next_line
                    i += 1
                    if i < len(lines) and ("youtube.com" in lines[i] or "youtu.be" in lines[i]):
                        url = lines[i]
                        i += 1

                # Gather lyric lines until the next song block or divider
                while i < len(lines):
                    l_text = lines[i]
                    if not l_text:
                        i += 1
                        continue
                    # Stop gathering if we hit a new potential title/divider pattern
                    if "youtube.com" in l_text or "youtu.be" in l_text:
                        break
                    content.append(l_text)
                    i += 1

                songs.append({
                    'title': title,
                    'artist': artist,
                    'youtube': url,
                    'is_sing_along': False,
                    'content': content
                })
                continue

        i += 1

    # Sort alphabetically by title
    songs = sorted(songs, key=lambda x: x['title'].lower())

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=2)

    print(f"SUCCESS: Cleaned and extracted {len(songs)} songs into {JSON_PATH}.")
    return songs

if __name__ == "__main__":
    parse_txt_library()