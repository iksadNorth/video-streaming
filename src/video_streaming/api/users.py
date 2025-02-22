from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.video_streaming.model import Users
from src.video_streaming.db.database import get_db, Session
from src.video_streaming.utils.jwt import get_user_login


router = APIRouter()


class UserReadResponse(BaseModel):
    nickname: str
    bedge_src: str
class UserUpdateRequest(BaseModel):
    nickname: str
class UserUpdateResponse(BaseModel):
    msg: str


@router.get("/users/me")
async def auth_google_callback(
        session: Session = Depends(get_db),
        user_loggedin: Users = Depends(get_user_login),
    ):
    user_res = UserReadResponse(
        nickname=user_loggedin.nickname,
        bedge_src=user_loggedin.bedge_src,
    )
    return user_res

@router.patch("/users/me")
async def auth_google_callback(
        item: UserUpdateRequest,
        session: Session = Depends(get_db),
        user_loggedin: Users = Depends(get_user_login),
    ):
    user_loggedin.nickname = item.nickname
    session.merge(user_loggedin)
    session.commit()
    
    return UserUpdateResponse(msg='변경완료.')
