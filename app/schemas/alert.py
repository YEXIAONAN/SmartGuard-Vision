from datetime import datetime

from typing import Literal

from pydantic import BaseModel, ConfigDict


class AlertBase(BaseModel):
    alert_code: str
    alert_type: str
    alert_level: str
    source_type: str
    location: str
    description: str
    status: str
    handled_by: str | None = None
    handling_note: str | None = None
    handled_at: datetime | None = None
    device_id: int | None = None


class AlertCreate(BaseModel):
    alert_type: str
    alert_level: str
    source_type: str
    location: str
    description: str
    status: str = "pending"
    handled_by: str | None = None
    handling_note: str | None = None
    handled_at: datetime | None = None
    device_id: int | None = None
    occurred_at: datetime | None = None


class AlertRead(AlertBase):
    id: int
    occurred_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertStatusUpdate(BaseModel):
    status: Literal["pending", "processing", "resolved"]
    handled_by: str | None = None
    handling_note: str | None = None
    handled_at: datetime | None = None
