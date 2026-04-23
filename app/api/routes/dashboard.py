from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.schemas.dashboard import DashboardOverview
from app.schemas.response import ApiResponse
from app.services.dashboard_service import get_dashboard_overview
from app.utils.response import success_response

router = APIRouter()


@router.get("/overview", response_model=ApiResponse[DashboardOverview], summary="首页总览数据")
def dashboard_overview(db: Session = Depends(get_db), _: object = Depends(get_current_user)):
    overview = get_dashboard_overview(db)
    return success_response(data=overview)
