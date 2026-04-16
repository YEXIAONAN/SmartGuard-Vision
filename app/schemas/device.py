from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DeviceBase(BaseModel):
    device_code: str
    device_name: str
    device_type: str
    location: str
    status: str
    is_online: bool


class DeviceCreate(DeviceBase):
    last_seen_at: datetime | None = None


class DeviceRead(DeviceBase):
    id: int
    last_seen_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
