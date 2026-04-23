from collections import defaultdict
from datetime import datetime, timedelta
from secrets import token_urlsafe
from threading import Lock

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.models.auth_refresh_token import AuthRefreshToken
from app.models.auth_revoked_token import AuthRevokedToken
from app.models.user import User

FAILED_LOGIN_ATTEMPTS: dict[str, list[datetime]] = defaultdict(list)
FAILED_LOGIN_LOCK = Lock()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.scalar(select(User).where(User.id == user_id))


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.scalar(select(User).where(User.username == username))


def _clean_failed_attempts(username: str) -> list[datetime]:
    window = datetime.utcnow() - timedelta(minutes=settings.auth_login_rate_window_minutes)
    attempts = [item for item in FAILED_LOGIN_ATTEMPTS[username] if item >= window]
    FAILED_LOGIN_ATTEMPTS[username] = attempts
    return attempts


def assert_login_allowed(username: str):
    with FAILED_LOGIN_LOCK:
        attempts = _clean_failed_attempts(username)
        if len(attempts) < settings.auth_login_rate_limit:
            return

        lock_since = attempts[-settings.auth_login_rate_limit]
        unlock_at = lock_since + timedelta(minutes=settings.auth_lock_minutes)
        if unlock_at > datetime.utcnow():
            raise PermissionError("登录失败次数过多，请稍后再试")


def mark_login_failed(username: str):
    with FAILED_LOGIN_LOCK:
        attempts = _clean_failed_attempts(username)
        attempts.append(datetime.utcnow())
        FAILED_LOGIN_ATTEMPTS[username] = attempts


def clear_login_failures(username: str):
    with FAILED_LOGIN_LOCK:
        if username in FAILED_LOGIN_ATTEMPTS:
            FAILED_LOGIN_ATTEMPTS.pop(username)


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(db, username)
    if user is None or not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def _create_refresh_token(db: Session, user: User) -> tuple[str, datetime]:
    expires_at = datetime.utcnow() + timedelta(days=settings.auth_refresh_token_expire_days)
    token = token_urlsafe(48)
    db.add(
        AuthRefreshToken(
            user_id=user.id,
            token=token,
            expires_at=expires_at,
            revoked=False,
        ),
    )
    return token, expires_at


def create_login_response(db: Session, user: User) -> dict:
    access_token, jti, access_expires_at = create_access_token(
        user_id=user.id,
        username=user.username,
        role=user.role,
    )
    refresh_token, refresh_expires_at = _create_refresh_token(db, user)
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": int((access_expires_at - datetime.utcnow()).total_seconds()),
        "refresh_token": refresh_token,
        "refresh_expires_in": int((refresh_expires_at - datetime.utcnow()).total_seconds()),
        "user": user,
        "jti": jti,
    }


def refresh_login_session(db: Session, refresh_token: str) -> dict | None:
    token_record = db.scalar(
        select(AuthRefreshToken).where(AuthRefreshToken.token == refresh_token),
    )
    if token_record is None or token_record.revoked:
        return None

    if token_record.expires_at < datetime.utcnow():
        token_record.revoked = True
        db.commit()
        return None

    user = get_user_by_id(db, token_record.user_id)
    if user is None or not user.is_active:
        token_record.revoked = True
        db.commit()
        return None

    token_record.revoked = True
    return create_login_response(db, user)


def revoke_refresh_token(db: Session, refresh_token: str):
    token_record = db.scalar(select(AuthRefreshToken).where(AuthRefreshToken.token == refresh_token))
    if token_record is None:
        return
    token_record.revoked = True
    db.commit()


def revoke_access_token(db: Session, jti: str, expires_at: datetime):
    if not jti:
        return
    db.add(AuthRevokedToken(jti=jti, expires_at=expires_at))
    db.commit()


def is_access_token_revoked(db: Session, jti: str) -> bool:
    if not jti:
        return True
    exists = db.scalar(select(AuthRevokedToken.id).where(AuthRevokedToken.jti == jti))
    return exists is not None


def cleanup_expired_auth_tokens(db: Session):
    now = datetime.utcnow()
    db.execute(delete(AuthRefreshToken).where(AuthRefreshToken.expires_at < now))
    db.execute(delete(AuthRevokedToken).where(AuthRevokedToken.expires_at < now))
    db.commit()


def seed_default_users(db: Session):
    default_users = [
        {
            "username": "admin",
            "password": "admin123",
            "display_name": "系统管理员",
            "role": "admin",
            "location_scope": None,
        },
        {
            "username": "operator",
            "password": "operator123",
            "display_name": "值班员",
            "role": "operator",
            "location_scope": None,
        },
        {
            "username": "viewer",
            "password": "viewer123",
            "display_name": "只读访客",
            "role": "viewer",
            "location_scope": None,
        },
    ]

    existing = {
        item.username: item
        for item in db.scalars(select(User).where(User.username.in_([u["username"] for u in default_users]))).all()
    }

    for item in default_users:
        user = existing.get(item["username"])
        if user is None:
            db.add(
                User(
                    username=item["username"],
                    password_hash=hash_password(item["password"]),
                    display_name=item["display_name"],
                    role=item["role"],
                    location_scope=item["location_scope"],
                    is_active=True,
                ),
            )
            continue

        user.display_name = item["display_name"]
        user.role = item["role"]
        user.location_scope = item["location_scope"]
        user.is_active = True
        user.password_hash = hash_password(item["password"])

    db.commit()
