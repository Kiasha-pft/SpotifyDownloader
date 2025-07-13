import os
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
DOWNLOAD_PATH = os.getenv('DOWNLOAD_PATH', 'downloads')
MAX_FILE_SIZE = 50 * 1024 * 1024
AUDIO_QUALITY = '320k'
MAX_SEARCH_RESULTS = 5
SEARCH_LANGUAGE = 'en'
def validate_config():
    required_vars = {
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
        'SPOTIPY_CLIENT_ID': SPOTIPY_CLIENT_ID,
        'SPOTIPY_CLIENT_SECRET': SPOTIPY_CLIENT_SECRET
    }
    missing_vars = [var for var, value in required_vars.items() if not value]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    return True 