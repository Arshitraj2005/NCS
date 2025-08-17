import subprocess
import os
import json
from dotenv import load_dotenv

load_dotenv()

STREAM_KEY = os.getenv("STREAM_KEY")
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

# ✅ Step 1: Extract video URLs from playlist
def get_playlist_videos(playlist_url):
    try:
        ydl_cmd = ["yt-dlp", "--flat-playlist", "-J", playlist_url]
        playlist_json = subprocess.check_output(ydl_cmd).decode()
        data = json.loads(playlist_json)
        return [f"https://www.youtube.com/watch?v={entry['id']}" for entry in data["entries"]]
    except subprocess.CalledProcessError:
        print("⚠️ Failed to fetch playlist data.")
        return []

# ✅ Step 2: Stream a single video
def stream_video(video_url):
    try:
        ydl_cmd = ["yt-dlp", "-f", "bestaudio[ext=mp4]/bestaudio", "-g", video_url]
        direct_url = subprocess.check_output(ydl_cmd).decode().strip()
    except subprocess.CalledProcessError:
        print(f"⚠️ Failed to fetch stream URL: {video_url}")
        return

    ffmpeg_cmd = [
        "ffmpeg", "-re", "-i", direct_url,
        "-c:a", "aac", "-b:a", "128k",
        "-f", "flv", RTMP_URL
    ]
    subprocess.run(ffmpeg_cmd)

# ✅ Step 3: Loop through playlist
def start_stream():
    playlist_url = "https://youtube.com/playlist?list=PLHr_15RHvVmlJm4fHysG-v5BW1JEPgOqa"
    video_urls = get_playlist_videos(playlist_url)

    while True:
        for video_url in video_urls:
            print(f"🎵 Streaming: {video_url}")
            stream_video(video_url)

if __name__ == "__main__":
    start_stream()
