import os
from typing import List

def load_previous_video_id(path: str) -> str:
    """Load the last processed video ID from a file, or return empty string if not found."""
    if not os.path.exists(path):
        return ""
    
    with open(path, "r") as file:
        return file.read().strip()


def save_video_ids(video_ids: List[str], path: str) -> None:
    """Save a list of links to a file, one per line."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, "w") as file:
        for id in video_ids:
            file.write(id.strip() + "\n")
