import re
import os
import logging
from urllib.parse import urlparse
from typing import Optional, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_title(title: str) -> str:
    return re.sub(r'[^\w\s\-\(\)\[\]]', '', title).strip()

def extract_spotify_id(url: str) -> Optional[str]:
    try:
        parsed = urlparse(url)
        if 'spotify.com' not in parsed.netloc:
            return None
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) >= 2:
            content_type = path_parts[0]
            content_id = path_parts[1].split('?')[0]
            if content_type in ['track', 'album', 'playlist'] and content_id:
                return (content_type, content_id)
    except Exception as e:
        logger.error(f"Error extracting Spotify ID: {e}")
    return None

def is_valid_spotify_url(url: str) -> bool:
    return extract_spotify_id(url) is not None

def create_search_query(artist: str, title: str) -> str:
    clean_artist = clean_title(artist)
    clean_title_text = clean_title(title)
    query = f"{clean_artist} - {clean_title_text} audio"
    return query

def ensure_download_directory(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created download directory: {directory}")

def format_file_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"

def sanitize_filename(filename: str) -> str:
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    filename = filename.strip(' .')
    if len(filename) > 200:
        filename = filename[:200]
    return filename

def get_file_extension(file_path: str) -> str:
    return os.path.splitext(file_path)[1].lower() 