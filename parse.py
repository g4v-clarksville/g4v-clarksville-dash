import re
import docx
import json

file_path = "SONGBOOK 344 (SAL) 0813.docx"
doc = docx.Document(file_path)

songs = []
current_song = None
parsing_started = False

# Words that instantly disqualify a line from being a song title
TOC_KEYWORDS = [
    "MAIN", "INDEX", "CONTENTS", "POP/ROCK", "BALLADS", "COUNTRY", 
    "CLASSIC", "UPBEAT", "SECTION", "TITLE", "GENRE", "ARTIST", "BY SONG", "TITLES IN RED"
]

for para in doc.paragraphs:
    text = para.text.strip().replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
    if not text:
        continue
    
    upper_text = text.upper()
    
    # Strict gate: Do not start parsing actual songs until we pass the index section.
    if not parsing_started:
        if "DIFFERENT DRUM" in upper_text and "LINDA" in upper_text:
            parsing_started = True
        else:
            continue

    # Skip any line that is purely decorative or an alphabet section divider
    if set(text) <= {'*', '-', '=', '_', ' ', '—', '.'}:
        continue
    if re.match(r'^\s*[-—]\s*[A-Z0-9]\s*[-—]\s*$', text):
        continue
    if any(keyword in upper_text for keyword in TOC_KEYWORDS):
        continue

    # Check for valid song header format (must contain a separator)
    if " — " in text or " - " in text:
        sep = " — " if " — " in text else " - "
        parts = text.split(sep, 1)
        
        if len(parts) == 2:
            title = parts[0].strip()
            artist = parts[1].strip()
            
            # Rigorous validation: both title and artist must look legitimate
            is_valid = (
                len(title) > 1 and 
                len(artist) > 1 and 
                not title.isdigit() and
                not artist.isdigit() and
                not title.startswith('(') and
                not any(kw in title.upper() for kw in TOC_KEYWORDS) and
                not any(kw in artist.upper() for kw in TOC_KEYWORDS)
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

    # If we are inside a valid song block, collect lyric lines
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