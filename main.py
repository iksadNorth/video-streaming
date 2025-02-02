from fastapi import FastAPI

from src.video_streaming.middleware.cors import cors
from src.video_streaming.api import video, metadata, comment


app = FastAPI()


# Router
app.include_router(video.router, prefix="/api/v1/video", tags=["video"])
app.include_router(metadata.router, prefix="/api/v1/metadata", tags=["metadata"])
app.include_router(comment.router, prefix="/api/v1/comments", tags=["comment"])

# MiddleWare
cors(app)


@app.get("/api/v1/health")
async def get_health():
    return {"code": "health"}
