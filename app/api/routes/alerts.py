from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.alert import AlertRead
from app.schemas.response import ApiResponse
from app.services.alert_service import list_alerts
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
