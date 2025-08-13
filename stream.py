import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

STREAM_KEY = os.getenv("STREAM_KEY")
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

# ✅ Your chosen video
VIDEO_URL = "https://www.youtube.com/watch?v=kbTUKUPjJY0"

def stream_video(video_url):
    try:
        ydl_cmd = [
            "yt-dlp", "-f", "bestaudio[ext=mp4]/bestaudio",
            "-g", video_url
        ]
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

def start_stream():
    while True:
        print(f"🎵 Streaming: {VIDEO_URL}")
        stream_video(VIDEO_URL)

if __name__ == "__main__":
    start_stream()
