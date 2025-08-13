import subprocess
import yt_dlp
import random
import os
from dotenv import load_dotenv

load_dotenv()

# Load your YouTube stream key securely
STREAM_KEY = os.getenv("STREAM_KEY")
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

# NCS playlist URL
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLRBp0Fe2GpgnIh0AiYKh7o7z3rGkJ0j6l"

def get_video_urls(playlist_url):
    """Fetch all video URLs from the playlist"""
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        entries = info.get('entries', [])
        urls = [entry['url'] for entry in entries if 'url' in entry]
        random.shuffle(urls)
        return urls

def stream_video(video_url):
    """Get direct audio URL and stream it via FFmpeg"""
    ydl_cmd = [
        "yt-dlp", "-f", "bestaudio[ext=mp4]/bestaudio",
        "-g", video_url
    ]
    direct_url = subprocess.check_output(ydl_cmd).decode().strip()

    ffmpeg_cmd = [
        "ffmpeg", "-re", "-i", direct_url,
        "-c:a", "aac", "-b:a", "128k",
        "-f", "flv", RTMP_URL
    ]
    subprocess.run(ffmpeg_cmd)

def start_stream():
    """Main loop to stream songs endlessly"""
    while True:
        urls = get_video_urls(PLAYLIST_URL)
        for url in urls:
            try:
                print(f"Streaming: {url}")
                stream_video(url)
            except Exception as e:
                print(f"Error streaming {url}: {e}")

if __name__ == "__main__":
    start_stream()
