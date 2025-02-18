from pydantic import BaseModel, Field
from fastapi import Query
from typing import Generic, TypeVar, List, Optional
from sqlalchemy.orm import Query as ormQuery

T = TypeVar("T")


class PaginationParams(BaseModel, Generic[T]):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)
    sort: Optional[str] = Query(None)
    
    def add_pages(self, query: ormQuery):
        return query.limit(self.page_size).offset((self.page - 1) * self.page_size)

    # 파라미터를 파싱해서 tuple({칼럼명},{asc|desc})로 출력
    # field '-created_at'
    # return tuple(created_at, desc)
    def get_sort(self):
        if not self.sort: 
            return None, None
        return self.sort.lstrip("-"), self.sort.startswith("-")

class PaginatedResponse(BaseModel, Generic[T]):
    totalCount: int
    page: int
    page_size: int
    items: List[T]
    
    @classmethod
    def from_query(cls, params: PaginationParams, query: ormQuery, post_process: callable = lambda x: x):
        items = params.add_pages(query).all()
        items: T = [post_process(item) for item in items]
        count: int = query.count()
        
        return PaginatedResponse(
            totalCount=count,
            page=params.page,
            page_size=params.page_size,
            items=items
        )

class SortLogic:
    @classmethod
    def add_sort(cls, query: ormQuery, column_name: str, is_asc=True):
        return query
    
    @classmethod
    def add_order_by(cls, query: ormQuery, new_order):
        existing_order = query._order_by_clauses
        return query.order_by(*existing_order, new_order)
