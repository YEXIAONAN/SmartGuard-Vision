from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SensorRecordBase(BaseModel):
    device_code: str
    sensor_type: str
    location: str
    temperature: float | None = None
    humidity: float | None = Field(default=None, ge=0, le=100)
    smoke_ppm: float | None = None
    risk_level: str = "low"
    payload: dict | None = None


class SensorRecordCreate(SensorRecordBase):
    reported_at: datetime | None = None


class SensorRecordRead(SensorRecordBase):
    id: int
    device_id: int | None = None
    reported_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
