from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.device import DeviceRead
from app.schemas.response import ApiResponse
from app.services.device_service import list_devices
from app.utils.response import success_response

router = APIRouter()


@router.get("", response_model=ApiResponse[list[DeviceRead]], summary="设备列表")
def get_devices(
    online_only: bool = Query(default=False, description="是否仅返回在线设备"),
    limit: int = Query(default=50, ge=1, le=200, description="返回条数"),
    db: Session = Depends(get_db),
):
    devices = list_devices(db, online_only=online_only, limit=limit)
    return success_response(data=devices)
