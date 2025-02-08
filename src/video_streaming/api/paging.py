from pydantic import BaseModel, Field
from typing import Generic, TypeVar, List
from sqlalchemy.orm import Query

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)  # 기본값 1, 1 이상만 허용
    page_size: int = Field(10, ge=1, le=100)  # 기본값 10, 1~100 허용
    
    def add_pages(self, query: Query):
        return query.limit(self.page_size).offset((self.page - 1) * self.page_size)

class PaginatedResponse(BaseModel, Generic[T]):
    totalCount: int
    page: int
    page_size: int
    items: List[T]
    
    @classmethod
    def from_query(cls, params: PaginationParams, query: Query, post_process: callable = lambda x: x):
        items = params.add_pages(query).all()
        items: T = [post_process(item) for item in items]
        count: int = query.count()
        
        return PaginatedResponse(
            totalCount=count,
            page=params.page,
            page_size=params.page_size,
            items=items
        )
