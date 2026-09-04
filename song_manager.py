import os
import json
import re

TXT_PATH = "song_library.txt"
JSON_PATH = "songs.json"

def parse_txt_library():
    if not os.path.exists(TXT_PATH):
        print(f"Error: Could not find {TXT_PATH}")
        return []

    print("Parsing song_library.txt...")
    with open(TXT_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match song blocks: Title, Artist, YouTube URL, followed by lyrics
    # Adjust this regex if your text file uses a slightly different layout
    pattern = re.compile(
        r'(?P<title>^[A-Z0-9\s\'’–()-]+)\n'
        r'(?P<artist>[A-Z][A-Za-z\s&,./()’-]+)\n\n'
        r'(?P<url>https://(?:www\.)?youtube\.com/watch\?v=[^\s]+.*)',
        re.MULTILINE
    )

    songs = []
    matches = list(pattern.finditer(content))
    
    for i, match in enumerate(matches):
        start_pos = match.start()
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        
        song_block = content[start_pos:end_pos].strip()
        lines = song_block.split('\n')
        
        title = match.group('title').strip()
        artist = match.group('artist').strip()
        url = match.group('url').strip()
        
        # Everything after URL is considered lyrics/content
        lyrics = []
        url_found = False
        for line in lines:
            if url in line:
                url_found = True
                continue
            if url_found:
                lyrics.append(line.strip())

        songs.append({
            'title': title,
            'artist': artist,
            'youtube': url,
            'content': [l for l in lyrics if l] # remove empty lines
        })

    # Sort alphabetically by song title
    songs = sorted(songs, key=lambda x: x['title'].lower())

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=2)

    print(f"SUCCESS: Extracted and sorted {len(songs)} songs alphabetically.")
    return songs

def interactive_search(songs):
    while True:
        print("\n=== Songbook Search Menu ===")
        print("1. Search by Song Title")
        print("2. Search by Artist")
        print("3. List All Songs Alphabetically")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            query = input("Enter title search term: ").strip().lower()
            results = [s for s in songs if query in s['title'].lower()]
            display_results(results)
        elif choice == '2':
            query = input("Enter artist search term: ").strip().lower()
            results = [s for s in songs if query in s['artist'].lower()]
            display_results(results)
        elif choice == '3':
            display_results(songs)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

def display_results(results):
    if not results:
        print("\nNo matching songs found.")
        return
        
    print(f"\nFound {len(results)} matching song(s):")
    for i, song in enumerate(results, 1):
        print(f"{i}. {song['title']} - {song['artist']}")
        
    choice = input("\nEnter song number to view details/lyrics (or press Enter to return): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(results):
        song = results[int(choice) - 1]
        print(f"\n=== {song['title']} by {song['artist']} ===")
        if song['youtube']:
            print(f"YouTube: {song['youtube']}")
        print("\nLyrics / Content:")
        if song['content']:
            print("\n".join(song['content']))
        else:
            print("No lyrics stored for this song.")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    if os.path.exists(JSON_PATH):
        load_choice = input("Found existing songs.json. Re-parse text file? (y/n): ").strip().lower()
        if load_choice == 'y':
            songs = parse_txt_library()
        else:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                songs = json.load(f)
            print(f"Loaded {len(songs)} songs from {JSON_PATH}.")
    else:
        songs = parse_txt_library()
        
    if songs:
        interactive_search(songs)