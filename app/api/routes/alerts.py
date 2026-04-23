from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_roles
from app.schemas.alert import AlertRead, AlertStatusUpdate
from app.schemas.alert_action import AlertActionRead
from app.schemas.pagination import PaginatedData
from app.schemas.response import ApiResponse
from app.services.alert_service import (
    export_alerts_csv,
    list_alert_action_logs,
    list_alerts,
    scan_and_escalate_overdue_alerts,
    update_alert_status,
)
from app.services.audit_service import log_audit_event
from app.utils.response import success_response

router = APIRouter()


@router.get("", response_model=ApiResponse[PaginatedData[AlertRead]], summary="告警列表")
def get_alerts(
    level: str | None = Query(default=None, description="告警等级过滤"),
    status: str | None = Query(default=None, description="处置状态过滤"),
    keyword: str | None = Query(default=None, description="关键字过滤"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    location_scope = current_user.location_scope if current_user.role in {"operator", "viewer"} else None
    items, total = list_alerts(
        db,
        level=level,
        status=status,
        keyword=keyword,
        page=page,
        page_size=page_size,
        location_scope=location_scope,
    )
    return success_response(data=PaginatedData(items=items, total=total, page=page, page_size=page_size))


@router.patch("/{alert_id}/status", response_model=ApiResponse[AlertRead], summary="更新告警处置状态")
def patch_alert_status(
    payload: AlertStatusUpdate,
    alert_id: int = Path(..., ge=1, description="告警 ID"),
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "operator")),
):
    if payload.status in {"processing", "resolved"}:
        if not payload.handled_by or not payload.handled_by.strip():
            raise HTTPException(status_code=422, detail="handled_by is required for processing/resolved status")
        if not payload.handling_note or not payload.handling_note.strip():
            raise HTTPException(status_code=422, detail="handling_note is required for processing/resolved status")

    alert = update_alert_status(
        db,
        alert_id=alert_id,
        status=payload.status,
        handled_by=payload.handled_by,
        handling_note=payload.handling_note,
        handled_at=payload.handled_at,
    )
    if alert is None:
        raise HTTPException(status_code=404, detail="alert not found")

    log_audit_event(
        db,
        username=current_user.username,
        role=current_user.role,
        action="alert.update_status",
        target_type="alert",
        target_id=str(alert_id),
        detail=f"更新状态为 {payload.status}",
    )
    return success_response(data=alert, message="alert status updated")


@router.get("/{alert_id}/actions", response_model=ApiResponse[list[AlertActionRead]], summary="告警处置审计日志")
def get_alert_actions(
    alert_id: int = Path(..., ge=1, description="告警 ID"),
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    logs = list_alert_action_logs(db, alert_id=alert_id)
    return success_response(data=logs)


@router.post("/sla/scan", response_model=ApiResponse[dict], summary="扫描并升级超时告警")
def scan_sla(db: Session = Depends(get_db), current_user=Depends(require_roles("admin", "operator"))):
    count = scan_and_escalate_overdue_alerts(db)
    log_audit_event(
        db,
        username=current_user.username,
        role=current_user.role,
        action="alert.sla_scan",
        target_type="alert",
        detail=f"本次升级 {count} 条告警",
    )
    return success_response(data={"escalated_count": count, "scanned_at": datetime.now()})


@router.get("/export/csv", summary="导出告警CSV")
def export_alerts(
    level: str | None = Query(default=None),
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    content = export_alerts_csv(db, current_user=current_user, level=level, status=status)
    log_audit_event(
        db,
        username=current_user.username,
        role=current_user.role,
        action="alert.export_csv",
        target_type="alert",
        detail=f"导出筛选 level={level or '*'}, status={status or '*'}",
    )
    return Response(
        content=content,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="alerts.csv"'},
    )
