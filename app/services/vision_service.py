from datetime import datetime

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.vision_record import VisionRecord
from app.schemas.alert import AlertCreate
from app.schemas.vision_record import VisionRecordCreate
from app.services.alert_service import create_alert
from app.services.device_service import get_device_by_code

HIGH_RISK_EVENTS = {"飞线充电", "明火", "电池拆卸充电"}
HIGH_RISK_LEVELS = {"high", "高风险"}
MEDIUM_RISK_LEVELS = {"medium", "中风险"}


def list_vision_records(
    db: Session,
    *,
    keyword: str | None = None,
    event_type: str | None = None,
    risk_level: str | None = None,
    limit: int = 50,
):
    stmt = select(VisionRecord).order_by(VisionRecord.reported_at.desc()).limit(limit)

    if keyword:
        fuzzy_keyword = f"%{keyword.strip()}%"
        stmt = stmt.where(
            or_(
                VisionRecord.device_code.ilike(fuzzy_keyword),
                VisionRecord.location.ilike(fuzzy_keyword),
                VisionRecord.event_type.ilike(fuzzy_keyword),
            )
        )
    if event_type:
        stmt = stmt.where(VisionRecord.event_type == event_type)
    if risk_level:
        stmt = stmt.where(VisionRecord.risk_level == risk_level)

    return db.scalars(stmt).all()


def get_vision_record_by_id(db: Session, record_id: int):
    stmt = select(VisionRecord).where(VisionRecord.id == record_id)
    return db.scalar(stmt)


def create_vision_record(db: Session, payload: VisionRecordCreate):
    device = get_device_by_code(db, payload.device_code)
    record = VisionRecord(
        device_id=device.id if device else None,
        device_code=payload.device_code,
        location=payload.location,
        image_url=payload.image_url,
        event_type=payload.event_type,
        risk_level=payload.risk_level,
        confidence=payload.confidence,
        detected_count=payload.detected_count,
        payload=payload.payload,
        reported_at=payload.reported_at or datetime.now(),
    )
    db.add(record)
    db.flush()

    if payload.event_type in HIGH_RISK_EVENTS or payload.risk_level in HIGH_RISK_LEVELS | MEDIUM_RISK_LEVELS:
        level = "high" if payload.event_type in HIGH_RISK_EVENTS or payload.risk_level in HIGH_RISK_LEVELS else "medium"
        create_alert(
            db,
            AlertCreate(
                alert_type=payload.event_type,
                alert_level=level,
                source_type="vision",
                location=payload.location,
                description=f"视觉识别到{payload.event_type}，建议尽快复核处置。",
                device_id=device.id if device else None,
                occurred_at=record.reported_at,
            ),
        )

    db.commit()
    db.refresh(record)
    return record
