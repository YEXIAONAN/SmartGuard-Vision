from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_roles
from app.schemas.pagination import PaginatedData
from app.schemas.response import ApiResponse
from app.schemas.vision_record import VisionRecordCreate, VisionRecordRead
from app.services.vision_service import (
    create_vision_record,
    get_vision_filter_options,
    get_vision_record_by_id,
    list_vision_records,
)
from app.utils.response import success_response

router = APIRouter()


@router.get("", response_model=ApiResponse[PaginatedData[VisionRecordRead]], summary="视觉识别历史列表")
def get_vision_records(
    keyword: str | None = Query(default=None, description="匹配设备编码/位置/事件类型"),
    event_type: str | None = Query(default=None, description="事件类型过滤"),
    risk_level: str | None = Query(default=None, description="风险等级过滤"),
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=20, ge=1, le=100, description="每页条数"),
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    records, total = list_vision_records(
        db,
        keyword=keyword,
        event_type=event_type,
        risk_level=risk_level,
        page=page,
        page_size=page_size,
    )
    return success_response(
        data=PaginatedData(items=records, total=total, page=page, page_size=page_size),
    )


@router.get("/filter-options", response_model=ApiResponse[dict[str, list[str]]], summary="视觉历史筛选项")
def get_vision_history_filter_options(
    keyword: str | None = Query(default=None, description="关键字过滤"),
    event_type: str | None = Query(default=None, description="事件类型过滤"),
    risk_level: str | None = Query(default=None, description="风险等级过滤"),
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    options = get_vision_filter_options(
        db,
        keyword=keyword,
        event_type=event_type,
        risk_level=risk_level,
    )
    return success_response(data=options)


@router.get("/{record_id}", response_model=ApiResponse[VisionRecordRead], summary="视觉识别记录详情")
def get_vision_record_detail(
    record_id: int = Path(..., ge=1, description="视觉记录 ID"),
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    record = get_vision_record_by_id(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="vision record not found")
    return success_response(data=record)


@router.post(
    "/report",
    response_model=ApiResponse[VisionRecordRead],
    status_code=status.HTTP_201_CREATED,
    summary="接收视觉识别结果",
)
def report_vision_result(
    payload: VisionRecordCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_roles("admin", "operator")),
):
    record = create_vision_record(db, payload)
    return success_response(data=record, message="vision record created")
