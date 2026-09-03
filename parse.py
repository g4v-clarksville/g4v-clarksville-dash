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
    
    # Absolute drop filters for any artifact, divider, or index page noise
    if set(text) <= {'*', '-', '=', '_', ' ', '—'}:
        continue
    if any(term in upper_text for term in ["INDEX", "TOC", "(MAIN)", "MAIN INDEX", "BY SONG TITLE", "ARTIST INDEX", "SONG INDEX"]):
        continue
    if re.match(r'^\s*-\s*[A-Z0-9]\s*-\s*$', text):
        continue
    if any(c in text for c in ["***", "==="]) or text.startswith("---"):
        continue

    # Check for valid Title - Artist header pattern
    if (" — " in text or " - " in text) and len(text) < 80:
        sep = " — " if " — " in text else " - "
        parts = text.split(sep, 1)
        
        if len(parts) == 2:
            title = parts[0].strip()
            artist = parts[1].strip()
            
            # Guard against metadata keywords slipping into the title/artist fields
            if any(kw in title.upper() or kw in artist.upper() for kw in ["INDEX", "MAIN", "TOC", "PAGE"]):
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

    # Append valid lyric lines to the active song
    if current_song:
        if not text.isdigit() and len(text) < 150:
            current_song["content"].append(text)

if current_song:
    songs.append(current_song)

# Save directly to songs.json since your HTML fetches it via fetch('songs.json')
with open("songs.json", "w", encoding="utf-8") as f:
    json.dump(songs, f, indent=2)

print(f"SUCCESS: Extracted exactly {len(songs)} valid songs to songs.json.")
print("First 3 songs found:")
for s in songs[:3]:
    print(f" - {s['title']} by {s['artist']}")