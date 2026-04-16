from datetime import datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.schemas.alert import AlertCreate


def list_alerts(db: Session, level: str | None = None, status: str | None = None, limit: int = 20):
    stmt = select(Alert).order_by(Alert.occurred_at.desc()).limit(limit)
    if level:
        stmt = stmt.where(Alert.alert_level == level)
    if status:
        stmt = stmt.where(Alert.status == status)
    return db.scalars(stmt).all()


def create_alert(db: Session, payload: AlertCreate):
    alert = Alert(
        alert_code=f"ALT-{datetime.now():%Y%m%d%H%M%S}-{uuid4().hex[:6].upper()}",
        alert_type=payload.alert_type,
        alert_level=payload.alert_level,
        source_type=payload.source_type,
        location=payload.location,
        description=payload.description,
        status=payload.status,
        device_id=payload.device_id,
        occurred_at=payload.occurred_at or datetime.now(),
    )
    db.add(alert)
    db.flush()
    return alert
