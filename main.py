from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from src.video_streaming.middleware.cors import cors
from src.video_streaming.api import video, comment, auth, users
from src.video_streaming.config import config
from src.video_streaming.middleware.logging import log_requests


app = FastAPI()


# Router
app.include_router(video.router, prefix="/api/v1", tags=["video"])
app.include_router(comment.router, prefix="/api/v1", tags=["comment"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])

# MiddleWare
cors(app)
app.middleware("http")(log_requests)

# 특정 폴더의 파일을 "/static" 경로에서 제공
static_path = Path(config('video.path'))
app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/api/v1/health")
async def get_health():
    return {"code": "health"}
