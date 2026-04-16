from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SensorRecord(Base):
    __tablename__ = "sensor_records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"), nullable=True)
    device_code: Mapped[str] = mapped_column(String(64), index=True)
    sensor_type: Mapped[str] = mapped_column(String(64), index=True)
    location: Mapped[str] = mapped_column(String(255))
    temperature: Mapped[float | None] = mapped_column(Float, nullable=True)
    humidity: Mapped[float | None] = mapped_column(Float, nullable=True)
    smoke_ppm: Mapped[float | None] = mapped_column(Float, nullable=True)
    risk_level: Mapped[str] = mapped_column(String(32), default="low", index=True)
    payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    reported_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    device = relationship("Device", back_populates="sensor_records")
