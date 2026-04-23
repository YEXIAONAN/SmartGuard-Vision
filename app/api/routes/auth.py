from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, parse_access_token
from app.schemas.auth import CurrentUserRead, LoginRequest, LoginResponse, LogoutRequest, RefreshTokenRequest
from app.schemas.response import ApiResponse
from app.services.audit_service import log_audit_event
from app.services.auth_service import (
    assert_login_allowed,
    authenticate_user,
    clear_login_failures,
    create_login_response,
    mark_login_failed,
    refresh_login_session,
    revoke_access_token,
    revoke_refresh_token,
)
from app.utils.response import success_response

router = APIRouter()


@router.post("/login", response_model=ApiResponse[LoginResponse], summary="用户登录")
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    try:
        assert_login_allowed(payload.username)
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(exc)) from exc

    user = authenticate_user(db, payload.username, payload.password)
    if user is None:
        mark_login_failed(payload.username)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

    clear_login_failures(payload.username)
    data = create_login_response(db, user)
    log_audit_event(
        db,
        username=user.username,
        role=user.role,
        action="auth.login",
        detail="用户登录成功",
        ip=request.client.host if request.client else None,
    )
    data.pop("jti", None)
    return success_response(data=data, message="login success")


@router.post("/refresh", response_model=ApiResponse[LoginResponse], summary="刷新登录态")
def refresh(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    data = refresh_login_session(db, payload.refresh_token)
    if data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh token invalid")
    data.pop("jti", None)
    return success_response(data=data, message="refresh success")


@router.post("/logout", response_model=ApiResponse[dict], summary="退出登录")
def logout(
    payload: LogoutRequest,
    token_payload: dict = Depends(parse_access_token),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if payload.refresh_token:
        revoke_refresh_token(db, payload.refresh_token)

    jti = token_payload.get("jti")
    exp = int(token_payload.get("exp", 0))
    if jti and exp > 0:
        revoke_access_token(db, jti=jti, expires_at=datetime.utcfromtimestamp(exp))

    log_audit_event(
        db,
        username=current_user.username,
        role=current_user.role,
        action="auth.logout",
        detail="用户主动退出登录",
    )
    return success_response(data={"success": True}, message="logout success")


@router.get("/me", response_model=ApiResponse[CurrentUserRead], summary="当前用户")
def me(current_user=Depends(get_current_user)):
    return success_response(data=current_user)
