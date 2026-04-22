from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    alert_code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    alert_type: Mapped[str] = mapped_column(String(64), index=True)
    alert_level: Mapped[str] = mapped_column(String(32), index=True)
    source_type: Mapped[str] = mapped_column(String(32), default="system")
    location: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="pending", index=True)
    handled_by: Mapped[str | None] = mapped_column(String(64), nullable=True)
    handling_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    handled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"), nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    device = relationship("Device", back_populates="alerts")
    action_logs = relationship("AlertActionLog", back_populates="alert", cascade="all, delete-orphan")
