from fastapi import FastAPI, HTTPException
import requests
import yt_dlp

app = FastAPI()

# Define the Render API URL and key
render_api_url = "https://api.render.com/deploy/srv-clippr4m411s73dst3l0?key=A7nj2iGIU2c"

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

def handle_401_error():
    # Make a request to the Render API when a 401 error occurs
    response = requests.get(render_api_url)
    # You can handle the response as needed
    return {"error": f"Received 401 error. Render API response: {response.text}"}

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
    try:
        info_dict = ydl.extract_info(video_url, download=False)
        format_url = info_dict.get('url')
        if format_url:
            return {"url": format_url, "reqUrl": reqUrl, "vidFormat": vidFormat}
        else:
            return {"url": "Not found", "reqUrl": reqUrl, "vidFormat": vidFormat}
    except yt_dlp.utils.DownloadError as e:
        # Check if the exception message contains "HTTP Error 401"
        if "HTTP Error 401" in str(e):
            return handle_401_error()
        else:
            # Re-raise the exception if it's not a 401 error
            raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/getf/")
async def read_item(videourl: str = 'https://www.dailymotion.com/video/x8pywti'):
    try:
        available_formats = get_video_formats(videourl)
        return {"video_url": videourl, "formats": available_formats}
    except yt_dlp.utils.DownloadError as e:
        # Check if the exception message contains "HTTP Error 401"
        if "HTTP Error 401" in str(e):
            return handle_401_error()
        else:
            # Re-raise the exception if it's not a 401 error
            raise HTTPException(status_code=500, detail="Internal Server Error")
