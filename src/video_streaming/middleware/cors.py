from fastapi.middleware.cors import CORSMiddleware
from src.video_streaming.config import config

def cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins = config('cors.allow_origins'),   # 모든 도메인 허용 (보안상 특정 도메인만 허용하는 것이 좋음)
        allow_credentials=True,
        allow_methods=["*"],                            # 모든 HTTP 메서드 허용 (GET, POST, PUT, DELETE 등)
        allow_headers=["*"],                            # 모든 HTTP 헤더 허용
    )
