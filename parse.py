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
    
    # Exclude strict index artifacts, section indicators, or dividers
    if text.upper() in ["(MAIN)", "MAIN INDEX", "BY SONG TITLE"] or re.match(r'^-\s*[A-Z]\s*-$', text):
        continue
    if any(c in text for c in ["***", "==="]) or text.startswith("---"):
        continue

    # Check if this paragraph is a new song header (Title - Artist format)
    if (" — " in text or " - " in text) and len(text) < 80:
        sep = " — " if " — " in text else " - "
        parts = text.split(sep, 1)
        
        if len(parts) == 2 and len(parts[0].strip()) > 1 and len(parts[1].strip()) > 1:
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

    # Append lyrics or content lines if we are inside a valid song block
    if current_song:
        if not text.isdigit() and len(text) < 150:
            current_song["content"].append(text)

if current_song:
    songs.append(current_song)

with open("songs.json", "w") as f:
    json.dump(songs, f, indent=2)

print(f"SUCCESS: Extracted exactly {len(songs)} valid songs.")