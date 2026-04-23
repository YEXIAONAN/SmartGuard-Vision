from datetime import datetime

from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.sensor_record import SensorRecord
from app.schemas.alert import AlertCreate
from app.schemas.sensor_record import SensorRecordCreate
from app.services.alert_service import create_alert
from app.services.device_service import get_device_by_code
from app.services.rule_service import get_rule_float


def apply_sensor_filters(
    stmt: Select,
    *,
    keyword: str | None = None,
    sensor_type: str | None = None,
    risk_level: str | None = None,
):
    if keyword:
        fuzzy_keyword = f"%{keyword.strip()}%"
        stmt = stmt.where(
            or_(
                SensorRecord.device_code.ilike(fuzzy_keyword),
                SensorRecord.location.ilike(fuzzy_keyword),
                SensorRecord.sensor_type.ilike(fuzzy_keyword),
            ),
        )
    if sensor_type:
        stmt = stmt.where(SensorRecord.sensor_type == sensor_type)
    if risk_level:
        stmt = stmt.where(SensorRecord.risk_level == risk_level)
    return stmt


def list_sensor_records(
    db: Session,
    *,
    keyword: str | None = None,
    sensor_type: str | None = None,
    risk_level: str | None = None,
    page: int = 1,
    page_size: int = 20,
):
    base_stmt = apply_sensor_filters(
        select(SensorRecord),
        keyword=keyword,
        sensor_type=sensor_type,
        risk_level=risk_level,
    )
    total_stmt = apply_sensor_filters(
        select(func.count()).select_from(SensorRecord),
        keyword=keyword,
        sensor_type=sensor_type,
        risk_level=risk_level,
    )

    records_stmt = (
        base_stmt.order_by(SensorRecord.reported_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    records = db.scalars(records_stmt).all()
    total = db.scalar(total_stmt) or 0
    return records, total


def get_sensor_filter_options(
    db: Session,
    *,
    keyword: str | None = None,
    sensor_type: str | None = None,
    risk_level: str | None = None,
):
    option_stmt = apply_sensor_filters(
        select(SensorRecord),
        keyword=keyword,
        sensor_type=sensor_type,
        risk_level=risk_level,
    )
    records = db.scalars(option_stmt).all()
    sensor_types = sorted({item.sensor_type for item in records if item.sensor_type})
    risk_levels = sorted({item.risk_level for item in records if item.risk_level})
    return {
        "sensor_types": sensor_types,
        "risk_levels": risk_levels,
    }


def get_sensor_record_by_id(db: Session, record_id: int):
    return db.scalar(select(SensorRecord).where(SensorRecord.id == record_id))


def create_sensor_record(db: Session, payload: SensorRecordCreate):
    device = get_device_by_code(db, payload.device_code)
    record = SensorRecord(
        device_id=device.id if device else None,
        device_code=payload.device_code,
        sensor_type=payload.sensor_type,
        location=payload.location,
        temperature=payload.temperature,
        humidity=payload.humidity,
        smoke_ppm=payload.smoke_ppm,
        risk_level=payload.risk_level,
        payload=payload.payload,
        reported_at=payload.reported_at or datetime.now(),
    )
    db.add(record)
    db.flush()

    temp_threshold = get_rule_float(db, "sensor_temp_threshold", settings.default_sensor_temp_threshold)
    smoke_threshold = get_rule_float(db, "sensor_smoke_threshold", settings.default_sensor_smoke_threshold)
    normalized_risk = str(payload.risk_level or "").lower()

    over_temperature = payload.temperature is not None and payload.temperature >= temp_threshold
    smoke_risk = payload.smoke_ppm is not None and payload.smoke_ppm >= smoke_threshold
    should_create_alert = over_temperature or smoke_risk or normalized_risk in {"high", "medium"}

    if should_create_alert:
        alert_level = "high" if over_temperature or smoke_risk or normalized_risk == "high" else "medium"
        create_alert(
            db,
            AlertCreate(
                alert_type="传感器异常",
                alert_level=alert_level,
                source_type="sensor",
                location=payload.location,
                description="接收到温度/烟雾异常上报，建议现场核查设备与停充环境。",
                device_id=device.id if device else None,
                occurred_at=record.reported_at,
            ),
        )

    db.commit()
    db.refresh(record)
    return record
