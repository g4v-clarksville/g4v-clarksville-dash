import os
import json
import re

TXT_PATH = "song_library.txt"
JSON_PATH = "songs.json"

def normalize_text(text):
    return re.sub(r'\s+', ' ', text).strip().lower()

def is_junk_title(title):
    clean = title.strip()
    if not clean or len(clean) > 60 or len(clean) < 2:
        return True
    if re.match(r'^[\s\-\–—_]*[A-Z0-9][\s\-\–—_]*$', clean, re.IGNORECASE):
        return True
    if set(clean) <= {'*', '-', '=', '_', ' ', '—', '.', '·', '(', ')', '[', ']'}:
        return True
    if clean.startswith('(') or clean.startswith('[') or clean.startswith('|') or clean.startswith('•'):
        return True
    if any(keyword in clean.upper() for keyword in ["MAIN INDEX", "BY ARTIST", "CONTENTS", "CHORD", "TAB", "TUNING", "CAPO"]):
        return True
    
    if re.match(r'^[A-G](?:#|b)?(?:\s+[A-G](?:#|b)?|\s+[0-9]+|\s+[\-\–—])+[\sA-G0-9\-\–—#b]*$', clean):
        return True
    if re.match(r'^[A-G](?:#|b)?(?:\s+[A-G0-9#b\-\–—]+)+$', clean, re.IGNORECASE):
        return True
    if re.match(r'^[A-G](?:#|b)?\s+[A-G](?:#|b)?m?', clean, re.IGNORECASE) and len(clean.split()) <= 3:
        return True

    if re.search(r'\b(ah+|oh+|la+|ha+|whop|humor)\b', clean, re.IGNORECASE) and len(re.findall(r'[a-zA-Z]+', clean)) < 4:
        return True
    if clean.lower().startswith("a little ") or clean.endswith("...") or clean.count('.') > 2:
        return True
        
    return False

def is_junk_artist(artist):
    clean = artist.strip()
    if not clean or clean.lower() == "unknown artist":
        return True
    if re.search(r'\b[0-9]+(?:\s*[\/\-\–—]\s*[0-9]+)+\b', clean):
        return True
    if re.search(r'[–—\-]{2,}', clean):
        return True
    if re.search(r'\b[A-G](?:#|b)?\b', clean) and any(c in clean for c in ['-', '—', '|', 'D', 'd']):
        return True
    if set(clean) <= {'|', '-', '—', ' ', 'D', 'd', 'b', 'O', 'o', '5', '4', '/'}:
        return True
    if len(clean) < 2 or len(clean) > 40:
        return True
    if clean.lower() in ["ah", "oh", "la", "ha", "unknown", "inst", "instrumental"]:
        return True
    if "faster" in clean.lower() or "slower" in clean.lower() or "tempo" in clean.lower():
        return True
    return False

def parse_txt_library():
    if not os.path.exists(TXT_PATH):
        print(f"Error: Could not find {TXT_PATH}")
        return []

    print("Parsing and cleaning song_library.txt with robust artist pattern matching...")
    with open(TXT_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [line.strip() for line in f.readlines()]

    songs_map = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line:
            i += 1
            continue

        if not is_junk_title(line):
            title = line
            artist = "Unknown Artist"
            youtube = ""
            lyrics = []
            
            i += 1
            scan_limit = min(i + 6, len(lines))
            while i < scan_limit:
                next_line = lines[i]
                if not next_line:
                    i += 1
                    continue
                
                if "youtube.com" in next_line or "youtu.be" in next_line:
                    if not youtube:
                        youtube = next_line.split()[0]
                    i += 1
                    continue
                
                # Bulletproof capture for "Artist: Name" or "By: Name" or direct lines
                artist_match = re.match(r'^(?:artist|by)\s*[:\-]?\s*(.+)$', next_line, re.IGNORECASE)
                if artist_match:
                    candidate = artist_match.group(1).strip()
                    if not is_junk_artist(candidate):
                        artist = candidate
                    i += 1
                    continue
                
                # If the line itself looks like a valid clean artist name immediately following the title
                if len(next_line) < 40 and not next_line.endswith('.') and not any(c in next_line for c in ['|', '[', '<', '—', '(', ')']):
                    if not is_junk_artist(next_line) and artist == "Unknown Artist":
                        artist = next_line
                        i += 1
                        continue
                
                break

            while i < len(lines):
                l = lines[i]
                if "youtube.com" in l or "youtu.be" in l:
                    if not youtube:
                        youtube = l.split()[0]
                    i += 1
                    continue
                if not l:
                    next_non_empty = None
                    for peek in range(i + 1, min(i + 4, len(lines))):
                        if lines[peek]:
                            next_non_empty = lines[peek]
                            break
                    if next_non_empty and not is_junk_title(next_non_empty):
                        break
                lyrics.append(l)
                i += 1

            if artist == "Unknown Artist" and lyrics:
                last_l = lyrics[-1].strip()
                artist_match = re.match(r'^(?:artist|by)\s*[:\-]?\s*(.+)$', last_l, re.IGNORECASE)
                if artist_match:
                    candidate = artist_match.group(1).strip()
                    if not is_junk_artist(candidate):
                        artist = candidate
                        lyrics.pop()
                elif not is_junk_artist(last_l) and len(last_l) < 30:
                    artist = last_l
                    lyrics.pop()

            clean_lyrics = [l for l in lyrics if l]
            
            if not clean_lyrics:
                continue

            norm_title = normalize_text(title)
            norm_artist = normalize_text(artist)

            if norm_title not in songs_map:
                songs_map[norm_title] = {
                    'title': title.strip(),
                    'artist': artist.strip(),
                    'youtube': youtube.strip(),
                    'is_sing_along': "sing-along" in title.lower() or "sing along" in artist.lower(),
                    'content': clean_lyrics
                }
            else:
                existing = songs_map[norm_title]
                if existing['artist'].lower() == "unknown artist" and artist.lower() != "unknown artist":
                    songs_map[norm_title] = {
                        'title': title.strip(),
                        'artist': artist.strip(),
                        'youtube': youtube.strip() or existing['youtube'],
                        'is_sing_along': "sing-along" in title.lower() or "sing along" in artist.lower(),
                        'content': clean_lyrics
                    }
        else:
            i += 1

    songs = list(songs_map.values())
    songs = sorted(songs, key=lambda x: x['title'].lower())

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=2)

    print(f"SUCCESS: Extracted, cleaned, and sorted {len(songs)} unique songs into {JSON_PATH}.")

if __name__ == "__main__":
    parse_txt_library()