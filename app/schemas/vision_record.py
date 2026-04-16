from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class VisionRecordBase(BaseModel):
    device_code: str
    location: str
    image_url: str | None = None
    event_type: str
    risk_level: str = "low"
    confidence: float | None = Field(default=None, ge=0, le=1)
    detected_count: int = Field(default=1, ge=0)
    payload: dict | None = None


class VisionRecordCreate(VisionRecordBase):
    reported_at: datetime | None = None


class VisionRecordRead(VisionRecordBase):
    id: int
    device_id: int | None = None
    reported_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
