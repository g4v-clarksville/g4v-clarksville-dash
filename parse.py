import re
import docx
import json

file_path = "SONGBOOK 344 (SAL) 0813.docx"
doc = docx.Document(file_path)

songs = []
current_song = None

for para in doc.paragraphs:
    text = para.text.strip().replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
    if not text:
        continue
    
    # 1. Absolute blocklist for TOC noise, dividers, and index markers
    upper_text = text.upper()
    if set(text) <= {'*', '-', '=', '_', ' ', '—'}:
        continue
    if any(marker in upper_text for marker in ["(MAIN)", "MAIN INDEX", "BY SONG TITLE", "ARTIST INDEX", "SONG INDEX", "THIS SONG"]):
        continue
    if re.match(r'^\s*-\s*[A-Z]\s*-\s*$', text):
        continue
    if any(c in text for c in ["***", "==="]) or text.startswith("---"):
        continue

    # 2. Check if this paragraph is a valid song header (Title - Artist format)
    if (" — " in text or " - " in text) and len(text) < 80:
        sep = " — " if " — " in text else " - "
        parts = text.split(sep, 1)
        
        if len(parts) == 2:
            title = parts[0].strip()
            artist = parts[1].strip()
            
            # Ensure neither part is a single-letter index marker or generic label
            if len(title) > 1 and len(artist) > 1 and not re.match(r'^-\s*[A-Z]\s*-$', title):
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

    # 3. Append lyrics or content lines if inside a valid song block
    if current_song:
        if not text.isdigit() and len(text) < 150:
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