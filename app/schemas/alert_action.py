from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertActionRead(BaseModel):
    id: int
    alert_id: int
    action_type: str
    from_status: str | None = None
    to_status: str | None = None
    handled_by: str | None = None
    handling_note: str | None = None
    handled_at: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
