import yt_dlp
import re
from typing import List


def get_latest_roundup(channel_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'playlistend': 10,
        'force_generic_extractor': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(channel_url + "/videos", download=False)
        if 'entries' in result:

            # Find the latest video with "Track Roundup" in the title
            # TODO: Make this more robust
            for entry in result['entries']:
                if 'Track Roundup' in entry.get('title', ''):
                    latest = entry
                    return {
                        'title': latest['title'],
                        'url': f"https://www.youtube.com/watch?v={latest['id']}",
                        'id': latest['id']
                    }
            raise Exception("No 'Weekly Roundup' videos found.")
        

def extract_url(line: str) -> str:
    line = line.strip()

    if "youtube.com" in line or "youtu.be" in line:
        return line  # already a full URL

    if line.startswith("/watch") or line.startswith("/shorts"):
        return f"https://www.youtube.com{line}"

    return ""  # Not a recognizable format


def extract_video_id(url: str) -> str:
    """
    Extract the 11-character YouTube video ID from a full or partial YouTube URL.
    """
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})(?:[&?]|\s|$)", url)
    return match.group(1) if match else ""

        

def extract_all_video_ids(description: str) -> List[str]:
    lines = description.replace("\r", "").split("\n")

    good, meh, bad = [], [], []
    current = None

    for line in lines:
        line_clean = line.strip().lower()

        # SECTION HEADERS
        if "!!!best" in line_clean or "best tracks" in line_clean:
            current = "good"
            continue
        elif "...meh" in line_clean:
            current = "meh"
            continue
        elif "!!!worst" in line_clean and "worst track" in line_clean:
            current = "bad"
            continue

        # Extract ID if this is a YouTube link
        match = re.search(r"(https?://)?(www\.)?(youtube\.com|youtu\.be|/[\w\-\_]+)", line, re.IGNORECASE)
        if match and current:
            url = extract_url(line)
            video_id = extract_video_id(url)
            if video_id:
                if current == "good":
                    good.append(video_id)
                elif current == "meh":
                    meh.append(video_id)
                elif current == "bad":
                    bad.append(video_id)

    return bad + meh + good

        
def extract_video_ids_from_description(video_url):
    ydl_opts = {
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        description = info.get('description', '')

        # Extract links from the description
        video_ids = extract_all_video_ids(description)
        return video_ids