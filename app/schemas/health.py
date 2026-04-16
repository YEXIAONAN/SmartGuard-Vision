from datetime import datetime

from pydantic import BaseModel


class HealthData(BaseModel):
    status: str
    service: str
    now: datetime
