#!/usr/bin/env python3
"""
Test script to verify the Spotify Telegram Bot setup.
Run this script to check if all dependencies and configurations are working.
"""

import sys
import os
import subprocess
from pathlib import Path

def test_python_version():
    """Test if Python version is compatible."""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported. Please use Python 3.8+")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True

def test_ffmpeg():
    """Test if FFmpeg is installed and accessible."""
    print("\n🎬 Testing FFmpeg installation...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg is installed and working")
            return True
        else:
            print("❌ FFmpeg is installed but not working properly")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg is not installed or not in PATH")
        print("   Please install FFmpeg:")
        print("   Windows: choco install ffmpeg or download from https://ffmpeg.org")
        print("   macOS: brew install ffmpeg")
        print("   Linux: sudo apt install ffmpeg")
        return False
    except subprocess.TimeoutExpired:
        print("❌ FFmpeg test timed out")
        return False

def test_python_dependencies():
    """Test if all Python dependencies can be imported."""
    print("\n📦 Testing Python dependencies...")
    
    dependencies = [
        ('telegram', 'python-telegram-bot'),
        ('spotipy', 'spotipy'),
        ('yt_dlp', 'yt-dlp'),
        ('youtubesearchpython', 'youtube-search-python'),
        ('mutagen', 'mutagen'),
        ('dotenv', 'python-dotenv'),
        ('requests', 'requests'),
        ('PIL', 'Pillow')
    ]
    
    all_good = True
    
    for module, package in dependencies:
        try:
            __import__(module)
            print(f"✅ {package} is installed")
        except ImportError as e:
            print(f"❌ {package} is not installed: {e}")
            all_good = False
    
    return all_good

def test_environment_file():
    """Test if .env file exists and has required variables."""
    print("\n🔧 Testing environment configuration...")
    
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found")
        print("   Please copy env.example to .env and fill in your credentials")
        return False
    
    # Load and check environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'TELEGRAM_TOKEN',
        'SPOTIPY_CLIENT_ID', 
        'SPOTIPY_CLIENT_SECRET'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your_'):
            missing_vars.append(var)
        else:
            print(f"✅ {var} is configured")
    
    if missing_vars:
        print(f"❌ Missing or invalid environment variables: {', '.join(missing_vars)}")
        print("   Please update your .env file with valid credentials")
        return False
    
    return True

def test_spotify_api():
    """Test Spotify API connection."""
    print("\n🎵 Testing Spotify API connection...")
    
    try:
        from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET
        import spotipy
        from spotipy.oauth2 import SpotifyClientCredentials
        
        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET
            )
        )
        
        # Test with a known track
        test_track = sp.track('4iV5W9uYEdYUVa79Axb7Rh')  # Bohemian Rhapsody
        if test_track:
            print("✅ Spotify API connection successful")
            print(f"   Test track: {test_track['name']} by {test_track['artists'][0]['name']}")
            return True
        else:
            print("❌ Spotify API returned no data")
            return False
            
    except Exception as e:
        print(f"❌ Spotify API connection failed: {e}")
        return False

def test_youtube_search():
    """Test YouTube search functionality."""
    print("\n📺 Testing YouTube search...")
    
    try:
        from youtubesearchpython import VideosSearch
        
        search = VideosSearch("Queen Bohemian Rhapsody", limit=1)
        results = search.result()
        
        if results and results.get('result'):
            print("✅ YouTube search is working")
            return True
        else:
            print("❌ YouTube search returned no results")
            return False
            
    except Exception as e:
        print(f"❌ YouTube search failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Spotify Telegram Bot Setup Test")
    print("=" * 40)
    
    tests = [
        test_python_version,
        test_ffmpeg,
        test_python_dependencies,
        test_environment_file,
        test_spotify_api,
        test_youtube_search
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("   You can now run: python bot.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above before running the bot.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 