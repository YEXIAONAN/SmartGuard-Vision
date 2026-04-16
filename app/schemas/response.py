from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class ApiResponse(BaseModel, Generic[DataT]):
    code: int = 0
    message: str = "success"
    data: DataT
    timestamp: datetime = Field(default_factory=datetime.now)
