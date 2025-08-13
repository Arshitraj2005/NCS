import subprocess
import random
import os
from dotenv import load_dotenv

load_dotenv()

STREAM_KEY = os.getenv("STREAM_KEY")
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

# ✅ Direct NCS video URLs (remove private ones!)
NCS_VIDEOS = [
    "https://www.youtube.com/watch?v=J2X5mJ3HDYE",  # Alan Walker - Fade
    "https://www.youtube.com/watch?v=7wNb0pHyGuI",  # Tobu - Hope
    "https://www.youtube.com/watch?v=RXLzvo6kvVQ",  # Janji - Heroes Tonight
    "https://www.youtube.com/watch?v=ZkqyIoYAXV8",  # Disfigure - Blank
    "https://www.youtube.com/watch?v=U1q1g1V9mSg",  # Elektronomia - Energy
    # ✅ Add more public links only
]

def stream_video(video_url):
    try:
        ydl_cmd = [
            "yt-dlp", "-f", "bestaudio[ext=mp4]/bestaudio",
            "-g", video_url
        ]
        direct_url = subprocess.check_output(ydl_cmd).decode().strip()
    except subprocess.CalledProcessError:
        print(f"⚠️ Skipping private or broken video: {video_url}")
        return

    ffmpeg_cmd = [
        "ffmpeg", "-re", "-i", direct_url,
        "-c:a", "aac", "-b:a", "128k",
        "-f", "flv", RTMP_URL
    ]
    subprocess.run(ffmpeg_cmd)

def start_stream():
    while True:
        random.shuffle(NCS_VIDEOS)
        for url in NCS_VIDEOS:
            print(f"🎵 Streaming: {url}")
            stream_video(url)

if __name__ == "__main__":
    start_stream()
