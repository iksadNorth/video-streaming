from fastapi import FastAPI

from src.video_streaming.middleware.cors import cors
from src.video_streaming.api import video, comment


app = FastAPI()


# Router
app.include_router(video.router, prefix="/api/v1", tags=["video"])
app.include_router(comment.router, prefix="/api/v1", tags=["comment"])

# MiddleWare
cors(app)


@app.get("/api/v1/health")
async def get_health():
    return {"code": "health"}
