from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
import aiofiles
from pathlib import Path

from src.video_streaming.model.BaseModel import BaseModel
from src.video_streaming.config import config


ROOT_DIR = Path(config('video.path'))

class Video(BaseModel):
    file_path  = Column(String, unique=True)
    thumbnail_path  = Column(String, unique=True)
    title = Column(String)
    
    publisher_id = Column(Integer, ForeignKey("users.id"))
    publisher = relationship("Users", back_populates="videos")
    
    comments = relationship("Comment", back_populates="video")


    @property
    def filePath(self) -> Path:
        return ROOT_DIR / self.file_path

    @filePath.setter
    def filePath(self, value: Path | str):
        self.file_path = str(value)

    async def range_stream(self, start: int, end: int):
        async with aiofiles.open(self.filePath, mode="rb") as f:
            await f.seek(start)
            remaining_bytes = end - start + 1
            while remaining_bytes > 0:
                chunk_size = min(1024 * 1024, remaining_bytes)
                data = await f.read(chunk_size)
                if not data:
                    break
                yield data
                remaining_bytes -= len(data)
