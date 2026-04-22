from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.response import ApiResponse
from app.schemas.sensor_record import SensorRecordCreate, SensorRecordRead
from app.services.sensor_service import create_sensor_record, get_sensor_record_by_id, list_sensor_records
from app.utils.response import success_response

router = APIRouter()


@router.get("", response_model=ApiResponse[list[SensorRecordRead]], summary="传感历史列表")
def get_sensor_records(
    keyword: str | None = Query(default=None, description="关键字过滤，匹配设备编码/位置/传感器类型"),
    sensor_type: str | None = Query(default=None, description="传感器类型过滤"),
    risk_level: str | None = Query(default=None, description="风险等级过滤"),
    limit: int = Query(default=50, ge=1, le=200, description="返回条数"),
    db: Session = Depends(get_db),
):
    records = list_sensor_records(
        db,
        keyword=keyword,
        sensor_type=sensor_type,
        risk_level=risk_level,
        limit=limit,
    )
    return success_response(data=records)


@router.get("/{record_id}", response_model=ApiResponse[SensorRecordRead], summary="传感记录详情")
def get_sensor_record_detail(
    record_id: int = Path(..., ge=1, description="传感记录 ID"),
    db: Session = Depends(get_db),
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
def report_sensor_result(payload: SensorRecordCreate, db: Session = Depends(get_db)):
    record = create_sensor_record(db, payload)
    return success_response(data=record, message="sensor record created")
