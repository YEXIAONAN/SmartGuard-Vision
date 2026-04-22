from datetime import datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.alert_action import AlertActionLog
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
        handled_by=payload.handled_by,
        handling_note=payload.handling_note,
        handled_at=payload.handled_at,
        device_id=payload.device_id,
        occurred_at=payload.occurred_at or datetime.now(),
    )
    db.add(alert)
    db.flush()
    return alert


def get_alert_by_id(db: Session, alert_id: int):
    stmt = select(Alert).where(Alert.id == alert_id)
    return db.scalar(stmt)


def list_alert_action_logs(db: Session, alert_id: int):
    stmt = select(AlertActionLog).where(AlertActionLog.alert_id == alert_id).order_by(AlertActionLog.created_at.desc())
    return db.scalars(stmt).all()


def update_alert_status(
    db: Session,
    alert_id: int,
    status: str,
    handled_by: str | None = None,
    handling_note: str | None = None,
    handled_at: datetime | None = None,
):
    alert = get_alert_by_id(db, alert_id)
    if not alert:
        return None

    previous_status = alert.status
    alert.status = status
    if handled_by is not None:
        alert.handled_by = handled_by.strip() or None
    if handling_note is not None:
        alert.handling_note = handling_note.strip() or None

    if status == "pending":
        alert.handled_at = None
        if handled_by is None:
            alert.handled_by = None
        if handling_note is None:
            alert.handling_note = None
    elif handled_at is not None:
        alert.handled_at = handled_at
    elif status == "resolved":
        alert.handled_at = datetime.now()

    action_log = AlertActionLog(
        alert_id=alert.id,
        action_type="status_update",
        from_status=previous_status,
        to_status=alert.status,
        handled_by=alert.handled_by,
        handling_note=alert.handling_note,
        handled_at=handled_at or datetime.now(),
    )
    db.add(action_log)

    db.commit()
    db.refresh(alert)
    return alert
