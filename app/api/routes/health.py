from datetime import datetime

from fastapi import APIRouter

from app.schemas.health import HealthData
from app.schemas.response import ApiResponse
from app.utils.response import success_response

router = APIRouter()


@router.get("/health", response_model=ApiResponse[HealthData], summary="服务健康检查")
def health_check():
    data = HealthData(status="ok", service="smartguard-vision-backend", now=datetime.now())
    return success_response(data=data, message="service is healthy")
