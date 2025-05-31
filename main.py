"""
main.py – Entry point for the Weekly Roundup Bot

Responsibilities:
- Load configuration
- Run scraping pipeline:
    1. Get latest video
    2. Extract comment links
    3. Update local song link file
    4. (Future) Sync with YT Music playlist
"""

import logging
from yt_scrape.scrape import get_latest_roundup, extract_video_ids_from_description
from utils.fileio import save_video_ids, load_previous_video_id
from yt_music.playlist_sync import get_ytmusic, clear_playlist, add_songs_to_playlist, update_playlist_description

# ---------- SETUP ----------

CHANNEL_URL = "https://www.youtube.com/@theneedledrop"
CACHE_FILE = "data/last_video.txt"
OUTPUT_FILE = "data/video_IDs.txt"
OUTPUT_PLAYLIST_ID = 'PLCbOev5SuUoliQ8OO-wbjBjglLnfm0FBX'

logging.basicConfig(level=logging.INFO)

# ---------- MAIN ----------

def main():
    yt_music = get_ytmusic()  # Initialize YT Music API client]

    logging.info("Checking for new video...")
    latest_roundup = get_latest_roundup(CHANNEL_URL)
    logging.info(f"Latest video: {latest_roundup['title']} ({latest_roundup['id']})")

    # Check if we already processed this video. If so we can exit because nothing new to do.
    last_video_id = load_previous_video_id(CACHE_FILE)
    if latest_roundup["id"] == last_video_id:
        logging.info("✅ No new video. Finished.")
        return
    logging.info(f"New video found: {latest_roundup['title']}")

    # IF there is a new video, extract links from the video description
    video_ids = extract_video_ids_from_description(latest_roundup["url"])
    save_video_ids(video_ids, OUTPUT_FILE)

    # Delete the old playlist and re-create an empty one
    logging.info("Cleaning existing playlist...")
    clear_playlist(yt_music, OUTPUT_PLAYLIST_ID)

    logging.info("Updating songs to playlist...")
    add_songs_to_playlist(yt_music, OUTPUT_PLAYLIST_ID, video_ids)
    update_playlist_description(yt_music, latest_roundup["title"], OUTPUT_PLAYLIST_ID)

    # Update cache file with the latest video ID
    logging.info(f"Uploaded {len(video_ids)} songs.")
    with open(CACHE_FILE, "w") as f:
        f.write(latest_roundup["id"])

    logging.info("✅ Done.")

# ---------- ENTRY POINT ----------

if __name__ == "__main__":
    main()
