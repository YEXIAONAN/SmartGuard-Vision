from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def log_audit_event(
    db: Session,
    *,
    username: str,
    role: str,
    action: str,
    target_type: str = "system",
    target_id: str | None = None,
    detail: str | None = None,
    ip: str | None = None,
):
    db.add(
        AuditLog(
            username=username,
            role=role,
            action=action,
            target_type=target_type,
            target_id=target_id,
            detail=detail,
            ip=ip,
        ),
    )
    db.commit()


def list_audit_logs(
    db: Session,
    *,
    username: str | None = None,
    action: str | None = None,
    page: int = 1,
    page_size: int = 20,
):
    stmt = select(AuditLog)
    total_stmt = select(func.count(AuditLog.id))

    if username:
        stmt = stmt.where(AuditLog.username == username)
        total_stmt = total_stmt.where(AuditLog.username == username)
    if action:
        stmt = stmt.where(AuditLog.action == action)
        total_stmt = total_stmt.where(AuditLog.action == action)

    logs = db.scalars(
        stmt.order_by(AuditLog.created_at.desc()).offset((page - 1) * page_size).limit(page_size),
    ).all()
    total = db.scalar(total_stmt) or 0
    return logs, total
