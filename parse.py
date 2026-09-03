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
    
    # 1. Immediate skips for artifacts, dividers, and TOC noise
    if set(text) <= {'*', '-', '=', '_', ' ', '—'}:
        continue
    if text.upper() in ["(MAIN)", "MAIN INDEX", "BY SONG TITLE", "ARTIST INDEX"]:
        continue
    if re.match(r'^-\s*[A-Z]\s*-$', text):
        continue
    if any(c in text for c in ["***", "==="]) or text.startswith("---"):
        continue

    # 2. Check for Song Header (Title - Artist)
    if (" — " in text or " - " in text) and len(text) < 80:
        sep = " — " if " — " in text else " - "
        parts = text.split(sep, 1)
        
        if len(parts) == 2 and len(parts[0].strip()) > 1 and len(parts[1].strip()) > 1:
            if not re.match(r'^-\s*[A-Z]\s*-$', parts[0].strip()) and not re.match(r'^-\s*[A-Z]\s*-$', parts[1].strip()):
                if current_song:
                    songs.append(current_song)
                
                is_red = any(run.font.color and run.font.color.rgb in [(255, 0, 0), (192, 0, 0)] for run in para.runs)
                
                current_song = {
                    "title": parts[0].strip(),
                    "artist": parts[1].strip(),
                    "is_sing_along": is_red,
                    "youtube": "",
                    "content": []
                }
                continue

    # 3. Append content lines if inside a valid song block
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