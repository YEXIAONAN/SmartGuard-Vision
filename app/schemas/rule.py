from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RuleConfigRead(BaseModel):
    id: int
    rule_key: str
    rule_value: str
    description: str | None = None
    updated_by: str | None = None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RuleConfigUpdate(BaseModel):
    rule_value: str
    description: str | None = None
