from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertBase(BaseModel):
    alert_code: str
    alert_type: str
    alert_level: str
    source_type: str
    location: str
    description: str
    status: str
    device_id: int | None = None


class AlertCreate(BaseModel):
    alert_type: str
    alert_level: str
    source_type: str
    location: str
    description: str
    status: str = "pending"
    device_id: int | None = None
    occurred_at: datetime | None = None


class AlertRead(AlertBase):
    id: int
    occurred_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
