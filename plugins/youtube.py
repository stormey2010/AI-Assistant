import requests
import yt_dlp
import os
from pygame import mixer
from config.config import *

def youtube_music(query):
    API_KEY = YOUTUBE_API_KEY
    music = query
    url = f'https://www.googleapis.com/youtube/v3/search?key={API_KEY}&part=snippet&type=video&q={music}'

    mixer.init()

    response = requests.get(url)
    data = response.json()

    if 'items' in data and len(data['items']) > 0:
        first_video_id = data['items'][0]['id']['videoId']
        print(f'First video ID: {first_video_id}')
        if os.path.exists('static/sound/music.mp3'):
            os.remove('static/sound/music.mp3')
        
        youtube_url = f'https://www.youtube.com/watch?v={first_video_id}'

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'static/sound/music',  # Output filename template
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': 'C:/PATH_FILES/ffmpeg.exe'  # Path to ffmpeg executable
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
            print(f'Downloaded and converted audio from {youtube_url} to mp3')
            return True
            
    else:
        print('No videos found.')
        return False
