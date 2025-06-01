from ytmusicapi import YTMusic
from dotenv import load_dotenv
import os

def get_ytmusic():
    # Load from .env only if not running on Railway
    if os.getenv("RAILWAY_ENVIRONMENT") is None:
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            raise ImportError("Missing 'python-dotenv")

    encoded_json = os.environ["BROWSER_JSON"]
    decoded_json = encoded_json.replace('\\"', '"').replace("\\n", "\n")

    os.makedirs("auth", exist_ok=True)
    with open("auth/browser.json", "w", encoding="utf-8") as f:
        f.write(decoded_json)

    return YTMusic("auth/browser.json")

import re
from datetime import datetime

def clear_playlist(ytmusic: YTMusic, playlist_id: str):
    playlist = ytmusic.get_playlist(playlist_id)
    items_to_remove = []

    for track in playlist.get("tracks", []):
        if "videoId" in track and "setVideoId" in track:
            items_to_remove.append({
                "videoId": track["videoId"],
                "setVideoId": track["setVideoId"]
            })

    if items_to_remove:
        ytmusic.remove_playlist_items(playlist_id, items_to_remove)

def update_playlist_description(ytmusic: YTMusic, title: str, playlist_id):
    # Grab last MM/DD/YY style date at the end of the title
    match = re.search(r"(\d{1,2}/\d{1,2}/\d{2,4})\s*$", title)
    if not match:
        return None

    raw_date = match.group(1)

    # Try both 2-digit and 4-digit year formats
    for fmt in ("%m/%d/%y", "%m/%d/%Y"):
        try:
            date_obj = datetime.strptime(raw_date, fmt)
            break
        except ValueError:
            continue
    else:
        return None

    readable = date_obj.strftime("%B %d, %Y")
    descripton = f"Weekly roundup for {readable} ordered worst to best"
    ytmusic.edit_playlist(
        playlistId=playlist_id,
        title=f"Fantano's Weekly Roundup – {readable}",
        description=descripton,
    )

def add_songs_to_playlist(ytmusic: YTMusic, playlist_id: str, video_ids: list):
    for video_id in video_ids:

        # Step 1: Get video title + artist
        info = ytmusic.get_song(video_id)
        details = info.get("videoDetails", {})
        if not details.get("title") or not details.get("author"):
            print(f"Missing title or author for: {video_id}")
            continue


        # Step 2: Retrieve the actual song and add to playlist
        query = f"{details.get('title', '')} {details.get('author', '')}"
        results = ytmusic.search(query, filter="songs")
        if results:
            song = results[0]
            title = song['title']
            artist = song['artists'][0]['name']
            song_id = song['videoId']

            # Step 3: Add the songs to the playlist
            print(f"🎵 Adding track: {title} by {artist}")
            ytmusic.add_playlist_items(playlist_id, [song_id])
            
        else:
            print(f"No matching song found for: {query}")


# Not used in this example, but can be useful for other scripts
# def get_playlist_id_by_name(ytmusic: YTMusic, name: str) -> str | None:
#     playlists = ytmusic.get_library_playlists(limit=100)
#     for pl in playlists:
#         if pl["title"].lower() == name.lower():
#             return pl["playlistId"]
#     return None
