from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import joinedload
from typing import Optional

from src.video_streaming.model import Comment, Users
from src.video_streaming.db.database import get_session, get_db, Session
from src.video_streaming.api.paging import PaginationParams, PaginatedResponse
from src.video_streaming.utils.jwt import get_user_login


router = APIRouter()


class CommentResponse(BaseModel):
    id: int
    comment: str
    src: Optional[str]
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
        .filter(Comment.video_id == video_id)
    
    sort_col, is_asc = page.get_sort()
    query = Comment.add_sort(query, sort_col, is_asc)
    
    def post_process(x: Comment):
        x = CommentResponse(
            id=x.id,
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

class CommentInsertReQuest(BaseModel):
    comment: str

@router.post("/videos/{video_id}/comments")
async def add_comment(
        video_id: str, 
        req: CommentInsertReQuest,
        session: Session = Depends(get_db),
        user_loggedin: Users = Depends(get_user_login),
    ):
    comment = Comment(
        comment=req.comment,
        publisher_id=user_loggedin.id,
        video_id=video_id,
    )
    session.add(comment)


@router.delete("/comments/{comment_id}")
async def add_comment(
        comment_id: str, 
        session: Session = Depends(get_db),
        user_loggedin: Users = Depends(get_user_login),
    ):
    if not user_loggedin:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    comment: Comment = session.query(Comment)\
        .filter(Comment.id == comment_id)\
        .first()
    if comment.publisher_id != user_loggedin.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    session.delete(comment)
