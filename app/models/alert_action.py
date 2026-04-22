from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class AlertActionLog(Base):
    __tablename__ = "alert_action_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    alert_id: Mapped[int] = mapped_column(ForeignKey("alerts.id"), index=True)
    action_type: Mapped[str] = mapped_column(String(32), default="status_update")
    from_status: Mapped[str | None] = mapped_column(String(32), nullable=True)
    to_status: Mapped[str | None] = mapped_column(String(32), nullable=True)
    handled_by: Mapped[str | None] = mapped_column(String(64), nullable=True)
    handling_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    handled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)

    alert = relationship("Alert", back_populates="action_logs")
