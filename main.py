from fastapi import FastAPI

import yt_dlp
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/dailymo/")
async def read_item(reqUrl: str = 'https://www.dailymotion.com/video/x8pdo3p', vidFormat: str='http-720-0'):
    
    video_url = reqUrl
    desired_format = vidFormat
    ydl_opts = {
        'quiet': True,  
        'format': desired_format,  
    }
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    info_dict = ydl.extract_info(video_url, download=False)
    format_url = info_dict.get('url')
    if format_url:
        return {"url":format_url,"reqUrl":reqUrl,"vidFormat":vidFormat}
    else:
        return {"url":"Not found","reqUrl":reqUrl,"vidFormat":vidFormat}   
