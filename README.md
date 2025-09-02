# Weekly Roundup Bot 🎵

Automatically sync songs from TheNeedleDrop's weekly music roundup videos to your YouTube Music playlist. Tracks are ordered worst to best. I deploy this on Railway using a CRON schedule so it automatically updates.

**Requirements:**
* Python 3.7+
* YouTube Music account with existing playlist
* YouTube Data API access

**Dependencies:**
* ytmusicapi (`pip install ytmusicapi`)
* yt-dlp (`pip install yt-dlp`) 
* youtube-comment-downloader (`pip install youtube-comment-downloader`)
* requests (`pip install requests`)
* Or install all at once: `pip install -r requirements.txt`

**How to Run:**

```
git clone https://github.com/JoeCamm/weeklyRoundup.git
cd weeklyRoundup
pip install -r requirements.txt
```

**Set up YouTube Music authentication:**
```python
# First time setup - follow ytmusicapi authentication guide
ytmusicapi oauth
```

**Configure your playlist:**
```python
# Edit main.py to set your playlist ID
OUTPUT_PLAYLIST_ID = 'your-playlist-id-here'
```

**Run the bot:**
```
python main.py
```

**Or run it automatically with cron:**
```bash
# Add to crontab for weekly automation
0 9 * * 1 cd /path/to/weeklyRoundup && python main.py
```

**What it does:**
1. Checks TheNeedleDrop channel for new weekly roundup videos
2. Extracts music video links from video descriptions  
3. Converts YouTube links to YouTube Music tracks
4. Updates your playlist with new songs
5. Maintains cache to avoid processing duplicate videos

**Output:**
- Updated YouTube Music playlist with latest roundup songs
- Log file showing processing status and song count
- Local cache of processed video IDs

**Note:** The bot only processes new videos since last run. If you want to reprocess a video, delete the cache file in `data/last_video.txt`.
