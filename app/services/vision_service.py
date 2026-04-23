from datetime import datetime

from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

from app.models.vision_record import VisionRecord
from app.schemas.alert import AlertCreate
from app.schemas.vision_record import VisionRecordCreate
from app.services.alert_service import create_alert
from app.services.device_service import get_device_by_code

HIGH_RISK_EVENTS = {"飞线充电", "明火", "电池拆卸充电"}


def apply_vision_filters(
    stmt: Select,
    *,
    keyword: str | None = None,
    event_type: str | None = None,
    risk_level: str | None = None,
):
    if keyword:
        fuzzy_keyword = f"%{keyword.strip()}%"
        stmt = stmt.where(
            or_(
                VisionRecord.device_code.ilike(fuzzy_keyword),
                VisionRecord.location.ilike(fuzzy_keyword),
                VisionRecord.event_type.ilike(fuzzy_keyword),
            ),
        )
    if event_type:
        stmt = stmt.where(VisionRecord.event_type == event_type)
    if risk_level:
        stmt = stmt.where(VisionRecord.risk_level == risk_level)
    return stmt


def list_vision_records(
    db: Session,
    *,
    keyword: str | None = None,
    event_type: str | None = None,
    risk_level: str | None = None,
    page: int = 1,
    page_size: int = 20,
):
    base_stmt = apply_vision_filters(
        select(VisionRecord),
        keyword=keyword,
        event_type=event_type,
        risk_level=risk_level,
    )
    total_stmt = apply_vision_filters(
        select(func.count()).select_from(VisionRecord),
        keyword=keyword,
        event_type=event_type,
        risk_level=risk_level,
    )

    records_stmt = (
        base_stmt.order_by(VisionRecord.reported_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    records = db.scalars(records_stmt).all()
    total = db.scalar(total_stmt) or 0
    return records, total


def get_vision_filter_options(
    db: Session,
    *,
    keyword: str | None = None,
    event_type: str | None = None,
    risk_level: str | None = None,
):
    option_stmt = apply_vision_filters(
        select(VisionRecord),
        keyword=keyword,
        event_type=event_type,
        risk_level=risk_level,
    )
    records = db.scalars(option_stmt).all()
    event_types = sorted({item.event_type for item in records if item.event_type})
    risk_levels = sorted({item.risk_level for item in records if item.risk_level})
    return {
        "event_types": event_types,
        "risk_levels": risk_levels,
    }


def get_vision_record_by_id(db: Session, record_id: int):
    return db.scalar(select(VisionRecord).where(VisionRecord.id == record_id))


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

    normalized_risk = str(payload.risk_level or "").lower()
    should_alert = payload.event_type in HIGH_RISK_EVENTS or normalized_risk in {"high", "medium"}
    if should_alert:
        alert_level = "high" if payload.event_type in HIGH_RISK_EVENTS or normalized_risk == "high" else "medium"
        create_alert(
            db,
            AlertCreate(
                alert_type=payload.event_type,
                alert_level=alert_level,
                source_type="vision",
                location=payload.location,
                description=f"视觉识别到“{payload.event_type}”，建议尽快复核处置。",
                device_id=device.id if device else None,
                occurred_at=record.reported_at,
            ),
        )

    db.commit()
    db.refresh(record)
    return record
