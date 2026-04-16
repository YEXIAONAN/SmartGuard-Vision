from datetime import datetime

from sqlalchemy.orm import Session

from app.models.vision_record import VisionRecord
from app.schemas.alert import AlertCreate
from app.schemas.vision_record import VisionRecordCreate
from app.services.alert_service import create_alert
from app.services.device_service import get_device_by_code

HIGH_RISK_EVENTS = {"飞线充电", "明火", "电池拆卸充电"}
HIGH_RISK_LEVELS = {"high", "高风险"}
MEDIUM_RISK_LEVELS = {"medium", "中风险"}


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
