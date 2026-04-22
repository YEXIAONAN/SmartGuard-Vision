from typing import Generic, TypeVar

from pydantic import BaseModel

ItemT = TypeVar("ItemT")


class PaginatedData(BaseModel, Generic[ItemT]):
    items: list[ItemT]
    total: int
    page: int
    page_size: int
