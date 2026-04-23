from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.schemas.auth import CurrentUserRead, LoginRequest, LoginResponse
from app.schemas.response import ApiResponse
from app.services.auth_service import authenticate_user, create_login_response
from app.utils.response import success_response

router = APIRouter()


@router.post("/login", response_model=ApiResponse[LoginResponse], summary="用户登录")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.username, payload.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

    return success_response(data=create_login_response(user), message="login success")


@router.get("/me", response_model=ApiResponse[CurrentUserRead], summary="当前用户")
def me(current_user=Depends(get_current_user)):
    return success_response(data=current_user)
