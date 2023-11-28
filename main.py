from fastapi import FastAPI

import yt_dlp
app = FastAPI()
def get_video_formats(video_url):
    formats_list = []
    
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        for format in info_dict.get('formats', []):
            format_info = {
                'format_id': format['format_id'],
                'ext': format['ext'],
                'resolution': format.get('resolution', ''),
            }
            formats_list.append(format_info)
    
    return formats_list

@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/dailymo/")
async def read_item(reqUrl: str = 'https://www.dailymotion.com/video/x8pywti', vidFormat: str='http-720-0'):
    
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
@app.get("/getf/")
async def read_item(videourl: str = 'https://www.dailymotion.com/video/x8pywti'):
    
    available_formats = get_video_formats(videourl)
    return {"video_url": videourl, "formats": available_formats}
