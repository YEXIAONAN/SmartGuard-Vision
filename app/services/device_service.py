from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.device import Device


def list_devices(db: Session, online_only: bool = False, limit: int = 50):
    stmt = select(Device).order_by(Device.id.desc()).limit(limit)
    if online_only:
        stmt = (
            select(Device)
            .where(Device.is_online.is_(True))
            .order_by(Device.last_seen_at.desc())
            .limit(limit)
        )
    return db.scalars(stmt).all()


def get_device_by_code(db: Session, device_code: str):
    stmt = select(Device).where(Device.device_code == device_code)
    return db.scalar(stmt)
