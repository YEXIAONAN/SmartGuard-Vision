from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.response import ApiResponse
from app.schemas.sensor_record import SensorRecordCreate, SensorRecordRead
from app.services.sensor_service import create_sensor_record
from app.utils.response import success_response

router = APIRouter()


@router.post(
    "/report",
    response_model=ApiResponse[SensorRecordRead],
    status_code=status.HTTP_201_CREATED,
    summary="接收传感器上报数据",
)
def report_sensor_result(payload: SensorRecordCreate, db: Session = Depends(get_db)):
    record = create_sensor_record(db, payload)
    return success_response(data=record, message="sensor record created")
