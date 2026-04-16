from datetime import datetime

from sqlalchemy.orm import Session

from app.models.sensor_record import SensorRecord
from app.schemas.alert import AlertCreate
from app.schemas.sensor_record import SensorRecordCreate
from app.services.alert_service import create_alert
from app.services.device_service import get_device_by_code


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

    over_temperature = payload.temperature is not None and payload.temperature >= 50
    smoke_risk = payload.smoke_ppm is not None and payload.smoke_ppm >= 10
    should_create_alert = over_temperature or smoke_risk or payload.risk_level in {"high", "高风险", "medium", "中风险"}

    if should_create_alert:
        alert_level = "high" if over_temperature or smoke_risk or payload.risk_level in {"high", "高风险"} else "medium"
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
