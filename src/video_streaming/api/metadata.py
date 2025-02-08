from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import joinedload

from src.video_streaming.db.database import get_session, Session
from src.video_streaming.model import Video


router = APIRouter()


class MetadateResponse(BaseModel):
    title: str
    publisher: str
    bdsrc: str
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
    
    return MetadateResponse(
        title=video.title,
        publisher=video.publisher.nickname,
        bdsrc=video.publisher.bedge_src,
        numDescripter=0,
        numLikes=0,
    )
