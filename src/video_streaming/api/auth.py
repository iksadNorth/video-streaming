from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import BaseModel
import requests
from src.video_streaming.config import config


router = APIRouter()


REDIRECT_URI = "http://localhost:3000/auth/google/callback"
TOKEN_URL = "https://oauth2.googleapis.com/token"
AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/auth"

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=AUTHORIZATION_URL,
    tokenUrl=TOKEN_URL
)

class Item(BaseModel):
    code: str

@router.post("/auth/google/callback")
async def auth_callback(item: Item):
    data = {
        "code": item.code,
        "client_id": config("oauth.google.client_id"),
        "client_secret": config("oauth.google.client_secret"),
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get token")

    token_info = response.json()
    access_token = token_info.get("access_token")
    
    # 사용자 정보 가져오기
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
    user_info = requests.get(USER_INFO_URL, headers={"Authorization": f"Bearer {access_token}"})
    if user_info.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get user info")

    result = user_info.json()
    result['access_token'] = 'test'
    print(result)
    return result