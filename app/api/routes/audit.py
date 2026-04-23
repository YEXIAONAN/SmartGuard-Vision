from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.schemas.audit import AuditLogRead
from app.schemas.pagination import PaginatedData
from app.schemas.response import ApiResponse
from app.services.audit_service import list_audit_logs
from app.utils.response import success_response

router = APIRouter()


@router.get("", response_model=ApiResponse[PaginatedData[AuditLogRead]], summary="审计日志列表")
def get_audit_logs(
    username: str | None = Query(default=None, description="按用户名过滤"),
    action: str | None = Query(default=None, description="按动作类型过滤"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: object = Depends(require_roles("admin")),
):
    logs, total = list_audit_logs(db, username=username, action=action, page=page, page_size=page_size)
    return success_response(data=PaginatedData(items=logs, total=total, page=page, page_size=page_size))
