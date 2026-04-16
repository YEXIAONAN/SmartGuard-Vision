from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    device_code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    device_name: Mapped[str] = mapped_column(String(100))
    device_type: Mapped[str] = mapped_column(String(50), index=True)
    location: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), default="normal")
    is_online: Mapped[bool] = mapped_column(Boolean, default=True)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    alerts = relationship("Alert", back_populates="device")
    vision_records = relationship("VisionRecord", back_populates="device")
    sensor_records = relationship("SensorRecord", back_populates="device")
