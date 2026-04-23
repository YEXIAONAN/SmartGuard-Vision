from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_roles
from app.schemas.pagination import PaginatedData
from app.schemas.response import ApiResponse
from app.schemas.sensor_record import SensorRecordCreate, SensorRecordRead
from app.services.sensor_service import (
    create_sensor_record,
    get_sensor_filter_options,
    get_sensor_record_by_id,
    list_sensor_records,
)
from app.utils.response import success_response

router = APIRouter()


@router.get("", response_model=ApiResponse[PaginatedData[SensorRecordRead]], summary="传感历史列表")
def get_sensor_records(
    keyword: str | None = Query(default=None, description="匹配设备编码/位置/传感器类型"),
    sensor_type: str | None = Query(default=None, description="传感器类型过滤"),
    risk_level: str | None = Query(default=None, description="风险等级过滤"),
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=20, ge=1, le=100, description="每页条数"),
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    records, total = list_sensor_records(
        db,
        keyword=keyword,
        sensor_type=sensor_type,
        risk_level=risk_level,
        page=page,
        page_size=page_size,
    )
    return success_response(
        data=PaginatedData(items=records, total=total, page=page, page_size=page_size),
    )


@router.get("/filter-options", response_model=ApiResponse[dict[str, list[str]]], summary="传感历史筛选项")
def get_sensor_history_filter_options(
    keyword: str | None = Query(default=None, description="关键字过滤"),
    sensor_type: str | None = Query(default=None, description="传感器类型过滤"),
    risk_level: str | None = Query(default=None, description="风险等级过滤"),
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    options = get_sensor_filter_options(
        db,
        keyword=keyword,
        sensor_type=sensor_type,
        risk_level=risk_level,
    )
    return success_response(data=options)


@router.get("/{record_id}", response_model=ApiResponse[SensorRecordRead], summary="传感记录详情")
def get_sensor_record_detail(
    record_id: int = Path(..., ge=1, description="传感记录 ID"),
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
):
    record = get_sensor_record_by_id(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="sensor record not found")
    return success_response(data=record)


@router.post(
    "/report",
    response_model=ApiResponse[SensorRecordRead],
    status_code=status.HTTP_201_CREATED,
    summary="接收传感器上报数据",
)
def report_sensor_result(
    payload: SensorRecordCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_roles("admin", "operator")),
):
    record = create_sensor_record(db, payload)
    return success_response(data=record, message="sensor record created")
