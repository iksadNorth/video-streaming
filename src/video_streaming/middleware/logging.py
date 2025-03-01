import time
from fastapi import Request
from starlette.responses import JSONResponse
from src.video_streaming.logger.log import logger

async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Request: {request.method} {request.url}")

    try:
        response = await call_next(request)  # 실제 요청 처리
        process_time = time.time() - start_time
        logger.info(f"Response: {response.status_code} ({process_time:.2f}s)")
        return response

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Error: {e} ({process_time:.2f}s)", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"}
        )
