import re
import docx
import json

file_path = "SONGBOOK 344 (SAL) 0813.docx"
doc = docx.Document(file_path)

songs = []
current_song = None
parsing_active = False

for para in doc.paragraphs:
    text = para.text.strip().replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
    if not text:
        continue
    
    upper_text = text.upper()
    
    # Do not start parsing real songs until we are safely past the entire index section.
    # We use the transition header for the very first actual song ("4 Non Blondes - What's Up?") as our gate.
    if not parsing_active:
        if "4 NON BLONDES" in upper_text or "WHAT’S UP" in upper_text or "DIFFERENT DRUM" in upper_text:
            # Make sure we are past the TOC by verifying it's deeper in the file or matching an actual song block format
            if " - " in text or " — " in text:
                parsing_active = True
        if not parsing_active:
            continue

    # Absolute blocklist for index artifacts, dividers, and junk lines
    if set(text) <= {'*', '-', '=', '_', ' ', '—', '.', '·'}:
        continue
    if re.match(r'^\s*[-—]\s*[A-Z0-9#]\s*[-—]\s*$', text):
        continue
    if text.startswith('(') or text.endswith(')'):
        continue
    if any(term in upper_text for term in ["MAIN INDEX", "BY ARTIST", "BY SONG TITLE", "CONTENTS", "POP/ROCK", "TITLES IN RED"]):
        continue

    # Check for valid song header format (Title - Artist)
    if " — " in text or " - " in text:
        sep = " — " if " — " in text else " - "
        parts = text.split(sep, 1)
        
        if len(parts) == 2:
            title = parts[0].strip()
            artist = parts[1].strip()
            
            # Strict validation to ensure it's a real song
            is_valid = (
                len(title) > 1 and 
                len(artist) > 1 and 
                not title.isdigit() and 
                not artist.isdigit() and
                not title.startswith('(') and
                not all(c in '*-=_— ' for c in title)
            )
            
            if is_valid:
                if current_song:
                    songs.append(current_song)
                
                is_red = any(run.font.color and run.font.color.rgb in [(255, 0, 0), (192, 0, 0)] for run in para.runs)
                
                current_song = {
                    "title": title,
                    "artist": artist,
                    "is_sing_along": is_red,
                    "youtube": "",
                    "content": []
                }
                continue

    # Collect lyrics if inside a valid song block
    if current_song:
        if len(text) < 150 and not text.isdigit():
            current_song["content"].append(text)

if current_song:
    songs.append(current_song)

with open("songs.json", "w", encoding="utf-8") as f:
    json.dump(songs, f, indent=2)

print(f"SUCCESS: Extracted exactly {len(songs)} valid songs and updated songs.json.")