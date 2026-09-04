import os
import json
import re

TXT_PATH = "song_library.txt"
JSON_PATH = "songs.json"

def clean_library():
    if not os.path.exists(TXT_PATH):
        print(f"Error: {TXT_PATH} not found.")
        return

    with open(TXT_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by song blocks (assuming standard format: Title, Artist, URL)
    pattern = re.compile(
        r'(?P<title>^[A-Z0-9\s\'’–()-]+)\n'
        r'(?P<artist>[A-Z][A-Za-z\s&,./()’-]+)\n\n'
        r'(?P<url>https://(?:www\.)?youtube\.com/watch\?v=[^\s]+.*)',
        re.MULTILINE
    )

    songs = []
    matches = list(pattern.finditer(content))
    
    for i, match in enumerate(matches):
        start_pos = match.start()
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        
        song_block = content[start_pos:end_pos].strip()
        lines = song_block.split('\n')
        
        title = match.group('title').strip()
        artist = match.group('artist').strip()
        url = match.group('url').strip()
        
        # Filter out index artifacts, dividers, and table headers
        is_junk = (
            set(title) <= {'*', '-', '=', '_', ' ', '—', '.', '·'} or
            title.startswith('(') or
            "****" in title or
            re.match(r'^\s*[-—]\s*[A-Z0-9#]\s*[-—]\s*$', title) or
            any(term in title.upper() for term in ["MAIN INDEX", "BY ARTIST", "CONTENTS"])
        )
        
        if is_junk:
            continue

        lyrics = []
        url_found = False
        for line in lines:
            if url in line:
                url_found = True
                continue
            if url_found:
                lyrics.append(line.strip())

        songs.append({
            'title': title,
            'artist': artist,
            'youtube': url,
            'is_sing_along': "sing-along" in title.lower() or "sing along" in artist.lower(), # adjust logic if needed
            'content': [l for l in lyrics if l]
        })

    # Sort alphabetically by title
    songs = sorted(songs, key=lambda x: x['title'].lower())

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=2)

    print(f"SUCCESS: Cleaned and saved {len(songs)} valid songs to {JSON_PATH}.")

if __name__ == "__main__":
    clean_library()