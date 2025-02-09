from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.video_streaming.middleware.cors import cors
from src.video_streaming.api import video, comment
from src.video_streaming.config import config


app = FastAPI()


# Router
app.include_router(video.router, prefix="/api/v1", tags=["video"])
app.include_router(comment.router, prefix="/api/v1", tags=["comment"])

# MiddleWare
cors(app)

# 특정 폴더의 파일을 "/static" 경로에서 제공
app.mount("/static", StaticFiles(directory=config('video.path')), name="static")


@app.get("/api/v1/health")
async def get_health():
    return {"code": "health"}
