from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import StreamingResponse
import os
from src.video_streaming.video import parse_range, range_stream

app = FastAPI()


@app.get("/api/v1/health")
async def get_health():
    return {"code": "health"}


@app.get("/api/v1/video/{video_id}")
async def get_video(video_id: str, request: Request):
    video_path = f"./video/{video_id}.mp4"
    
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
    
    file_size = os.path.getsize(video_path)
    range_header = request.headers.get("range")
    start, end = parse_range(range_header, file_size)
        
    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Content-Length": str(end - start + 1),
        "Accept-Ranges": "bytes",
        "Content-Type": "video/mp4",
    }
    
    return StreamingResponse(range_stream(video_path, start, end), headers=headers, status_code=206)
