from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import joinedload

from src.video_streaming.model import Comment
from src.video_streaming.db.database import get_session, Session
from src.video_streaming.api.paging import PaginationParams, PaginatedResponse


router = APIRouter()


class CommentResponse(BaseModel):
    comment: str
    src: str
    nickname: str
    created_at: datetime

@router.get("/videos/{video_id}/comments")
async def get_comments(
        video_id: str, 
        session: Session = Depends(get_session), 
        page: PaginationParams = Depends(),
    ):
    query: Query = session.query(Comment)\
        .options(joinedload(Comment.publisher))\
        .filter(Comment.video_id == video_id)\
        .order_by(Comment.created_at.desc())
    
    def post_process(x: Comment):
        x = CommentResponse(
            comment=x.comment.strip(), 
            src=x.publisher.bedge_src, 
            nickname=x.publisher.nickname, 
            created_at=x.created_at
        )
        return x
    
    return PaginatedResponse.from_query(
        params=page,
        query=query,
        post_process=post_process,
    )
