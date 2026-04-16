from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.response import ApiResponse
from app.schemas.vision_record import VisionRecordCreate, VisionRecordRead
from app.services.vision_service import create_vision_record
from app.utils.response import success_response

router = APIRouter()


@router.post(
    "/report",
    response_model=ApiResponse[VisionRecordRead],
    status_code=status.HTTP_201_CREATED,
    summary="接收视觉识别结果",
)
def report_vision_result(payload: VisionRecordCreate, db: Session = Depends(get_db)):
    record = create_vision_record(db, payload)
    return success_response(data=record, message="vision record created")
