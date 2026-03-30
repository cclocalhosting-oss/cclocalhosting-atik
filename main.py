from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import yt_dlp
import os
from urllib.parse import quote

app = FastAPI(title="All Video Downloader")

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.get("/info")
async def get_video_info(url: str):
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            formats = []
            for f in info.get('formats', []):
                if f.get('vcodec') != 'none' and f.get('height'):
                    formats.append({
                        "format_id": f.get('format_id'),
                        "quality": f.get('height'),
                        "ext": f.get('ext')
                    })
            
            return {
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration'),
                "formats": formats[:15]  # সব ফরম্যাট না দেখিয়ে ১৫টা
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/download")
async def download_video(url: str, format_id: str = None):
    try:
        filename = "video.%(ext)s"
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, filename),
            'format': format_id if format_id else 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=file_path,
            filename=os.path.basename(file_path),
            media_type="application/octet-stream"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
