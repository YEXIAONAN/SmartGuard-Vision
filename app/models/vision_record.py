from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class VisionRecord(Base):
    __tablename__ = "vision_records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"), nullable=True)
    device_code: Mapped[str] = mapped_column(String(64), index=True)
    location: Mapped[str] = mapped_column(String(255))
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    event_type: Mapped[str] = mapped_column(String(64), index=True)
    risk_level: Mapped[str] = mapped_column(String(32), index=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    detected_count: Mapped[int] = mapped_column(Integer, default=1)
    payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    reported_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    device = relationship("Device", back_populates="vision_records")
