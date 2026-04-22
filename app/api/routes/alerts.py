from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.alert import AlertRead, AlertStatusUpdate
from app.schemas.response import ApiResponse
from app.services.alert_service import list_alerts, update_alert_status
from app.utils.response import success_response

router = APIRouter()


@router.get("", response_model=ApiResponse[list[AlertRead]], summary="告警列表")
def get_alerts(
    level: str | None = Query(default=None, description="告警等级过滤"),
    status: str | None = Query(default=None, description="处置状态过滤"),
    limit: int = Query(default=20, ge=1, le=100, description="返回条数"),
    db: Session = Depends(get_db),
):
    alerts = list_alerts(db, level=level, status=status, limit=limit)
    return success_response(data=alerts)


@router.patch("/{alert_id}/status", response_model=ApiResponse[AlertRead], summary="更新告警处置状态")
def patch_alert_status(
    payload: AlertStatusUpdate,
    alert_id: int = Path(..., ge=1, description="告警 ID"),
    db: Session = Depends(get_db),
):
    alert = update_alert_status(db, alert_id=alert_id, status=payload.status)
    if alert is None:
        raise HTTPException(status_code=404, detail="alert not found")
    return success_response(data=alert, message="alert status updated")
