import logging
from logging.handlers import TimedRotatingFileHandler
from src.video_streaming.config import config


log_file = config('app.log_path')

handler = TimedRotatingFileHandler(
    log_file, when="midnight", interval=1, encoding="utf-8"
)  # 매일 자정마다 새로운 로그 파일 생성

handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())
