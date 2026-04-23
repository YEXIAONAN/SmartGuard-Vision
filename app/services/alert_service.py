from datetime import datetime, timedelta
from io import StringIO
from uuid import uuid4

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.alert_action import AlertActionLog
from app.models.user import User
from app.schemas.alert import AlertCreate
from app.services.rule_service import get_rule_int


def apply_alert_filters(
    stmt: Select,
    *,
    level: str | None = None,
    status: str | None = None,
    keyword: str | None = None,
    location_scope: str | None = None,
):
    if level:
        stmt = stmt.where(Alert.alert_level == level)
    if status:
        stmt = stmt.where(Alert.status == status)
    if keyword:
        like_keyword = f"%{keyword.strip()}%"
        stmt = stmt.where(
            Alert.location.ilike(like_keyword) | Alert.alert_type.ilike(like_keyword) | Alert.description.ilike(like_keyword),
        )
    if location_scope:
        stmt = stmt.where(Alert.location.ilike(f"%{location_scope}%"))
    return stmt


def list_alerts(
    db: Session,
    *,
    level: str | None = None,
    status: str | None = None,
    keyword: str | None = None,
    page: int = 1,
    page_size: int = 20,
    location_scope: str | None = None,
):
    base_stmt = apply_alert_filters(
        select(Alert),
        level=level,
        status=status,
        keyword=keyword,
        location_scope=location_scope,
    )
    total_stmt = apply_alert_filters(
        select(func.count(Alert.id)),
        level=level,
        status=status,
        keyword=keyword,
        location_scope=location_scope,
    )

    items = db.scalars(
        base_stmt.order_by(Alert.occurred_at.desc()).offset((page - 1) * page_size).limit(page_size),
    ).all()
    total = db.scalar(total_stmt) or 0
    return items, total


def create_alert(db: Session, payload: AlertCreate):
    occurred_at = payload.occurred_at or datetime.now()
    sla_minutes = get_rule_int(db, "alert_sla_minutes", 30)
    alert = Alert(
        alert_code=f"ALT-{datetime.now():%Y%m%d%H%M%S}-{uuid4().hex[:6].upper()}",
        alert_type=payload.alert_type,
        alert_level=payload.alert_level,
        source_type=payload.source_type,
        location=payload.location,
        description=payload.description,
        status=payload.status,
        handled_by=payload.handled_by,
        handling_note=payload.handling_note,
        handled_at=payload.handled_at,
        device_id=payload.device_id,
        occurred_at=occurred_at,
        sla_due_at=occurred_at + timedelta(minutes=sla_minutes),
    )
    db.add(alert)
    db.flush()
    return alert


def get_alert_by_id(db: Session, alert_id: int):
    return db.scalar(select(Alert).where(Alert.id == alert_id))


def list_alert_action_logs(db: Session, alert_id: int):
    stmt = select(AlertActionLog).where(AlertActionLog.alert_id == alert_id).order_by(AlertActionLog.created_at.desc())
    return db.scalars(stmt).all()


def update_alert_status(
    db: Session,
    alert_id: int,
    status: str,
    handled_by: str | None = None,
    handling_note: str | None = None,
    handled_at: datetime | None = None,
):
    alert = get_alert_by_id(db, alert_id)
    if not alert:
        return None

    previous_status = alert.status
    now = datetime.now()

    alert.status = status
    if handled_by is not None:
        alert.handled_by = handled_by.strip() or None
    if handling_note is not None:
        alert.handling_note = handling_note.strip() or None

    if status == "pending":
        alert.handled_at = None
        alert.first_response_at = None
        alert.resolved_at = None
    elif status == "processing":
        if alert.first_response_at is None:
            alert.first_response_at = handled_at or now
    elif status == "resolved":
        alert.handled_at = handled_at or now
        if alert.first_response_at is None:
            alert.first_response_at = handled_at or now
        alert.resolved_at = handled_at or now

    action_log = AlertActionLog(
        alert_id=alert.id,
        action_type="status_update",
        from_status=previous_status,
        to_status=alert.status,
        handled_by=alert.handled_by,
        handling_note=alert.handling_note,
        handled_at=handled_at or now,
    )
    db.add(action_log)

    db.commit()
    db.refresh(alert)
    return alert


def scan_and_escalate_overdue_alerts(db: Session):
    now = datetime.now()
    overdue = db.scalars(
        select(Alert).where(
            Alert.status != "resolved",
            Alert.sla_due_at.is_not(None),
            Alert.sla_due_at < now,
            Alert.escalated_at.is_(None),
        ),
    ).all()
    if not overdue:
        return 0

    for alert in overdue:
        alert.escalated_at = now
        if alert.status == "pending":
            alert.status = "processing"
            if not alert.handling_note:
                alert.handling_note = "系统自动升级：超过SLA时限未处理。"
        db.add(
            AlertActionLog(
                alert_id=alert.id,
                action_type="sla_escalation",
                from_status=alert.status,
                to_status=alert.status,
                handled_by="system",
                handling_note="告警超过SLA时限，已自动升级并催办。",
                handled_at=now,
            ),
        )
    db.commit()
    return len(overdue)


def export_alerts_csv(db: Session, *, current_user: User, level: str | None = None, status: str | None = None) -> str:
    location_scope = current_user.location_scope if current_user.role in {"operator", "viewer"} else None
    items, _ = list_alerts(
        db,
        level=level,
        status=status,
        page=1,
        page_size=2000,
        location_scope=location_scope,
    )
    buffer = StringIO()
    buffer.write("告警编号,告警类型,风险等级,位置,状态,发生时间,处理人,处理时间,处置备注\n")
    for item in items:
        buffer.write(
            f"{item.alert_code},{item.alert_type},{item.alert_level},{item.location},{item.status},"
            f"{item.occurred_at.strftime('%Y-%m-%d %H:%M:%S')},{item.handled_by or ''},"
            f"{item.handled_at.strftime('%Y-%m-%d %H:%M:%S') if item.handled_at else ''},{(item.handling_note or '').replace(',', '，')}\n",
        )
    return buffer.getvalue()
