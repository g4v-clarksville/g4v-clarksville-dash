import os
import json
import re

TXT_PATH = "song_library.txt"
JSON_PATH = "songs.json"

def parse_txt_library():
    if not os.path.exists(TXT_PATH):
        print(f"Error: Could not find {TXT_PATH}")
        return []

    with open(TXT_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        raw_content = f.read()

    # Split the library into blocks based on common separator patterns or double-newlines
    # This keeps entire song text chunks together cleanly
    blocks = re.split(r'\n\s*\n', raw_content)
    songs = []

    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue

        # Filter out alphabetical section headers like "- C -", "- D -" entirely
        if len(lines) == 1 and re.match(r'^[\-\–—\s]*[A-Z][\-\–—\s]*$', lines[0]):
            continue

        title = ""
        artist = "Unknown Artist"
        youtube = ""
        content_lines = []

        valid_lines = []
        for line in lines:
            # Check for YouTube links embedded anywhere in the block
            if "youtube.com" in line or "youtu.be" in line:
                youtube = line
                continue
            
            # Skip standalone section header markers
            if re.match(r'^[\-\–—\s]*[A-Z][\-\–—\s]*$', line):
                continue
                
            valid_lines.append(line)

        if not valid_lines:
            continue

        # The first valid line is our title
        potential_title = valid_lines[0]
        
        # Guard against picking garbage lines as titles
        if len(potential_title) > 60 or potential_title.startswith('(') or potential_title.startswith('[') or potential_title.startswith('|'):
            continue
            
        title = potential_title
        remaining_lines = valid_lines[1:]

        # Look for an artist name in the immediate next few lines or at the very end
        if remaining_lines:
            # Check if the second line is an artist (short, no punctuation ending, no chords)
            if len(remaining_lines[0]) < 35 and not remaining_lines[0].endswith('.') and not any(c in remaining_lines[0] for c in ['|', '[', '<', '—', '(', ')']):
                artist = remaining_lines[0]
                content_lines = remaining_lines[1:]
            else:
                content_lines = remaining_lines

        # If artist is still unknown, check the final line of the song body
        if artist == "Unknown Artist" and content_lines:
            last_line = content_lines[-1]
            if len(last_line) < 35 and not any(c in last_line for c in ['|', '[', '<', '(', ')']):
                artist = last_line
                content_lines.pop() # Remove it so it doesn't show up in the lyrics view

        # Final sanity check: skip if title is just a single letter artifact or pure punctuation
        stripped_title_core = re.sub(r'[\s\-\–—_#*]+', '', title)
        if len(stripped_title_core) <= 1:
            continue

        songs.append({
            'title': title,
            'artist': artist,
            'youtube': youtube,
            'is_sing_along': False,
            'content': content_lines
        })

    songs = sorted(songs, key=lambda x: x['title'].lower())

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=2)

    print(f"SUCCESS: Saved {len(songs)} cleanly parsed songs into {JSON_PATH}.")
    return songs

if __name__ == "__main__":
    parse_txt_library()