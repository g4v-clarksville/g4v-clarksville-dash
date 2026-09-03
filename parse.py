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
    
    upper_text = text.upper()
    
    # Comprehensive blacklist for all index markers, TOC headers, and artifacts
    if set(text) <= {'*', '-', '=', '_', ' ', '—'}:
        continue
    if any(term in upper_text for term in ["INDEX", "TOC", "(MAIN)", "MAIN INDEX", "BY SONG TITLE", "ARTIST INDEX", "SONG INDEX", "THIS SONG"]):
        continue
    if re.match(r'^\s*-\s*[A-Z0-9]\s*-\s*$', text):
        continue
    if any(c in text for c in ["***", "==="]) or text.startswith("---"):
        continue

    # Strict Song Header check: Must contain separator and NOT be an index line
    if (" — " in text or " - " in text) and len(text) < 80:
        sep = " — " if " — " in text else " - "
        parts = text.split(sep, 1)
        
        if len(parts) == 2:
            title = parts[0].strip()
            artist = parts[1].strip()
            
            # Ensure neither side contains index metadata keywords
            invalid_keywords = ["INDEX", "MAIN", "TOC", "PAGE", "SLIDE"]
            if any(kw in title.upper() or kw in artist.upper() for kw in invalid_keywords):
                continue
                
            if len(title) > 1 and len(artist) > 1:
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

    # Append content lines if inside a valid song block
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

print(f"SUCCESS: Extracted exactly {len(songs)} valid songs and updated data_v2.js.")