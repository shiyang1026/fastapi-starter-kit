from pydantic import BaseModel


class Response[T](BaseModel):
    code: int = 0
    message: str = "success"
    data: T | None = None


class PageResponse[T](BaseModel):
    """分页响应"""

    code: int = 0
    message: str = "success"
    data: T | None = None
    page_index: int
    page_size: int
    total: int


class CursorResponse[T](BaseModel):
    """游标分页响应"""

    code: int = 0
    message: str = "success"
    data: list[T]
    has_more: bool
    next_cursor: str | None = None
