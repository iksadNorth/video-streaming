from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.video_streaming.config import config
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = config('auth.access_token.secret_key')
ALGORITHM = config('auth.access_token.algorithm')
ACCESS_TOKEN_EXPIRE_SECONDS = config('auth.access_token.expiration_second')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
