from typing import Union

from fastapi import FastAPI

import youtube_dl
app = FastAPI()

@app.get("/")
def read_root():
    video_url = 'https://www.dailymotion.com/video/x8pdo3p'
    desired_format = 'http-720-0'
    ydl_opts = {
        'quiet': True,  
        'format': desired_format,  
    }
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    info_dict = ydl.extract_info(video_url, download=False)
    format_url = info_dict.get('url')
    if format_url:
        return {"url":format_url}
    else:
        return {"url":"Not found"}   
