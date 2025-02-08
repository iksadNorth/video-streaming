from sqlalchemy import Column, DateTime, BigInteger
from sqlalchemy.orm import declared_attr, declarative_base
from sqlalchemy.sql import func


# 기본적인 Base 클래스 생성
class BaseModel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()  # 테이블 이름을 모델 이름 소문자로 설정
    
    id = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)


# Base 클래스 재정의
BaseModel = declarative_base(cls=BaseModel)
