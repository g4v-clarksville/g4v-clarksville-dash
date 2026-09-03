import re
import docx
import json

file_path = "SONGBOOK 344 (SAL) 0813.docx"
doc = docx.Document(file_path)

songs = []
current_song = None
parsing_started = False

# Strict blocklist for anything that is metadata, a table of contents marker, or an alphabet divider
EXCLUDED_TERMS = [
    "MAIN", "INDEX", "CONTENTS", "POP/ROCK", "BALLADS", "COUNTRY", 
    "CLASSIC", "UPBEAT", "SECTION", "TITLE", "GENRE", "ARTIST", "BY SONG"
]

for para in doc.paragraphs:
    text = para.text.strip().replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
    if not text:
        continue
    
    upper_text = text.upper()
    
    # Skip everything until we hit the actual body of the songbook
    if not parsing_started:
        if "DIFFERENT DRUM" in upper_text or "A KISS AT THE END OF THE RAINBOW" in upper_text:
            parsing_started = True
        else:
            continue

    # Skip lines made entirely of punctuation, symbols, or single letters/alphabet markers (e.g., - C -, - T -)
    if set(text) <= {'*', '-', '=', '_', ' ', '—', '.'}:
        continue
    if re.match(r'^\s*[-—]\s*[A-Z0-9]\s*[-—]\s*$', text):
        continue
    if any(term in upper_text for term in EXCLUDED_TERMS):
        continue

    # Check for a valid song header format (must contain a separator)
    if " — " in text or " - " in text:
        sep = " — " if " — " in text else " - "
        parts = text.split(sep, 1)
        
        if len(parts) == 2:
            title = parts[0].strip()
            artist = parts[1].strip()
            
            # Rigorous checks to ensure it's an actual song and not an index artifact
            is_valid_song = (
                len(title) > 2 and 
                len(artist) > 2 and 
                not title.isdigit() and
                not artist.isdigit() and
                not re.match(r'^[A-Z]\s*$', title) and
                not any(term in title.upper() for term in EXCLUDED_TERMS) and
                not any(term in artist.upper() for term in EXCLUDED_TERMS)
            )
            
            if is_valid_song:
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

    # If we have an active song, append valid lyric lines
    if current_song:
        if len(text) < 150 and not text.isdigit():
            current_song["content"].append(text)

if current_song:
    songs.append(current_song)

with open("songs.json", "w", encoding="utf-8") as f:
    json.dump(songs, f, indent=2)

with open("data.js", "w", encoding="utf-8") as f:
    f.write("const songData = ")
    json.dump(songs, f, indent=2)
    f.write(";")

print(f"SUCCESS: Extracted exactly {len(songs)} valid songs and updated data.js.")