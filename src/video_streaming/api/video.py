from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import joinedload, Query
from typing import Optional

from src.video_streaming.config import config
from src.video_streaming.model import Video
from src.video_streaming.db.database import get_session, Session
from src.video_streaming.api.paging import PaginationParams, PaginatedResponse


router = APIRouter()


def parse_range(range_header, file_size):
    if not range_header:
        return 0, file_size - 1
    range_str = range_header.replace("bytes=", "").strip()
    start, end = range_str.split("-")[:2] if "-" in range_str else (int(range_str or 0), file_size - 1)
    start   = int(start)    if start    else 0
    end     = int(end)      if end      else file_size - 1
    return start, end

@router.get("/videos/{video_id}")
async def get_video(request: Request, video_id: str, session: Session = Depends(get_session)):
    video: Video = session.query(Video).filter(Video.id == video_id).first()
    
    if not video or not video.filePath or not video.filePath.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    
    file_size = video.filePath.stat().st_size
    range_header = request.headers.get("range")
    start, end = parse_range(range_header, file_size)
        
    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Content-Length": str(end - start + 1),
        "Accept-Ranges": "bytes",
        "Content-Type": "video/mp4",
    }

    return StreamingResponse(video.range_stream(start, end), headers=headers, status_code=206)

class VideoUnitResponse(BaseModel):
    title: str
    publisher: str
    bdsrc: Optional[str]
    numDescripter: int
    numLikes: int

@router.get("/videos/{video_id}/metadatas")
async def get_metadata(
        video_id: str, 
        session: Session = Depends(get_session),
    ):
    video: Video = session.query(Video)\
        .options(joinedload(Video.publisher))\
        .filter(Video.id == video_id)\
        .first()
    
    return VideoUnitResponse(
        title=video.title,
        publisher=getattr(video.publisher, 'nickname', ''),
        bdsrc=getattr(video.publisher, 'bedge_src', None),
        numDescripter=0,
        numLikes=0,
    )

class VideoArrResponse(BaseModel):
    videoId: int
    thumbnail: Optional[str]
    title: str
    publisher: str
    bdsrc: Optional[str]
    numViews: int
    created_at: datetime

@router.get("/videos")
async def get_video_arr(
        keyword: Optional[str],
        session: Session = Depends(get_session), 
        page: PaginationParams = Depends(),
    ):
    query: Query = session.query(Video)\
        .options(joinedload(Video.publisher))
    
    if keyword:
        query = query.filter(Video.title.ilike(f'%{keyword}%'))
    
    sort_col, is_asc = page.get_sort()
    query = Video.add_sort(query, sort_col, is_asc)
    
    app_url = config('app.url')
    def post_process(x: Video):
        x = VideoArrResponse(
            videoId=x.id,
            thumbnail=f'{app_url}/static/{x.thumbnail_path}',
            title=x.title.strip(),
            publisher=getattr(x.publisher, 'nickname', ''),
            bdsrc=getattr(x.publisher, 'bedge_src', None),
            numViews=0,
            created_at=x.created_at,
        )
        return x
    
    return PaginatedResponse.from_query(
        params=page,
        query=query,
        post_process=post_process,
    )
