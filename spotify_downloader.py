import os
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
import yt_dlp
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC
import requests
from typing import Optional, Dict, Any, Tuple
from PIL import Image
import io
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, DOWNLOAD_PATH, AUDIO_QUALITY
from utils import clean_title, create_search_query, ensure_download_directory, sanitize_filename, format_file_size, logger

class SpotifyDownloader:
    def __init__(self):
        self.spotify = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET
            )
        )
        ensure_download_directory(DOWNLOAD_PATH)
        self.cookiefile = 'cookies.txt' if os.path.exists('cookies.txt') else None

    def get_track_info(self, track_id: str) -> Optional[Dict[str, Any]]:
        try:
            track = self.spotify.track(track_id)
            track_info = {
                'id': track['id'],
                'name': track['name'],
                'artist': track['artists'][0]['name'] if track['artists'] else 'Unknown Artist',
                'album': track['album']['name'],
                'duration_ms': track['duration_ms'],
                'album_art_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'release_date': track['album']['release_date'],
                'popularity': track['popularity']
            }
            logger.info(f"Retrieved track info: {track_info['artist']} - {track_info['name']}")
            return track_info
        except Exception as e:
            logger.error(f"Error getting track info: {e}")
            return None

    def search_youtube(self, artist: str, title: str) -> Optional[str]:
        try:
            search_query = create_search_query(artist, title)
            logger.info(f"Searching YouTube for: {search_query}")
            videos_search = VideosSearch(search_query, limit=5)
            results = videos_search.result()
            if not results or not results.get('result'):
                logger.warning("No YouTube results found")
                return None
            video = results['result'][0]
            video_url = f"https://www.youtube.com/watch?v={video['id']}"
            logger.info(f"Found YouTube video: {video['title']}")
            return video_url
        except Exception as e:
            logger.error(f"Error searching YouTube: {e}")
            return None

    def download_audio(self, youtube_url: str, output_filename: str) -> Optional[str]:
        try:
            output_path = os.path.join(DOWNLOAD_PATH, f"{output_filename}.mp3")
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_path.replace('.mp3', '.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': AUDIO_QUALITY,
                }],
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            if self.cookiefile:
                ydl_opts['cookiefile'] = self.cookiefile
            logger.info(f"Downloading audio from: {youtube_url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                logger.info(f"Downloaded: {output_filename} ({format_file_size(file_size)})")
                return output_path
            else:
                logger.error("Download completed but file not found")
                return None
        except Exception as e:
            logger.error(f"Error downloading audio: {e}")
            return None

    def add_metadata(self, file_path: str, track_info: Dict[str, Any]) -> bool:
        try:
            audio = MP3(file_path)
            if audio.tags is None:
                audio.tags = ID3()
            audio.tags.add(TIT2(encoding=3, text=track_info['name']))
            audio.tags.add(TPE1(encoding=3, text=track_info['artist']))
            audio.tags.add(TALB(encoding=3, text=track_info['album']))
            if track_info.get('album_art_url'):
                try:
                    response = requests.get(track_info['album_art_url'])
                    if response.status_code == 200:
                        img = Image.open(io.BytesIO(response.content))
                        img_byte_arr = io.BytesIO()
                        img.save(img_byte_arr, format='JPEG')
                        img_byte_arr = img_byte_arr.getvalue()
                        audio.tags.add(APIC(
                            encoding=3,
                            mime='image/jpeg',
                            type=3,
                            desc='Cover',
                            data=img_byte_arr
                        ))
                        logger.info("Added album art to MP3")
                except Exception as e:
                    logger.warning(f"Could not add album art: {e}")
            audio.save()
            logger.info("Metadata added successfully")
            return True
        except Exception as e:
            logger.error(f"Error adding metadata: {e}")
            return False

    def download_track(self, spotify_url: str) -> Optional[Tuple[str, Dict[str, Any]]]:
        try:
            from utils import extract_spotify_id
            spotify_data = extract_spotify_id(spotify_url)
            if not spotify_data or spotify_data[0] != 'track':
                logger.error("Invalid Spotify track URL")
                return None
            track_id = spotify_data[1]
            track_info = self.get_track_info(track_id)
            if not track_info:
                return None
            youtube_url = self.search_youtube(track_info['artist'], track_info['name'])
            if not youtube_url:
                return None
            filename = sanitize_filename(f"{track_info['artist']} - {track_info['name']}")
            file_path = self.download_audio(youtube_url, filename)
            if not file_path:
                return None
            self.add_metadata(file_path, track_info)
            return file_path, track_info
        except Exception as e:
            logger.error(f"Error in download_track: {e}")
            return None

    def cleanup_file(self, file_path: str) -> None:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning up file: {e}") 