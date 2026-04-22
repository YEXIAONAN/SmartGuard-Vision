from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.response import ApiResponse
from app.schemas.vision_record import VisionRecordCreate, VisionRecordRead
from app.services.vision_service import create_vision_record, get_vision_record_by_id, list_vision_records
from app.utils.response import success_response

router = APIRouter()


@router.get("", response_model=ApiResponse[list[VisionRecordRead]], summary="视觉识别历史列表")
def get_vision_records(
    keyword: str | None = Query(default=None, description="关键字过滤，匹配设备编码/位置/事件类型"),
    event_type: str | None = Query(default=None, description="事件类型过滤"),
    risk_level: str | None = Query(default=None, description="风险等级过滤"),
    limit: int = Query(default=50, ge=1, le=200, description="返回条数"),
    db: Session = Depends(get_db),
):
    records = list_vision_records(
        db,
        keyword=keyword,
        event_type=event_type,
        risk_level=risk_level,
        limit=limit,
    )
    return success_response(data=records)


@router.get("/{record_id}", response_model=ApiResponse[VisionRecordRead], summary="视觉识别记录详情")
def get_vision_record_detail(
    record_id: int = Path(..., ge=1, description="视觉记录 ID"),
    db: Session = Depends(get_db),
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
def report_vision_result(payload: VisionRecordCreate, db: Session = Depends(get_db)):
    record = create_vision_record(db, payload)
    return success_response(data=record, message="vision record created")
