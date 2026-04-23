from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.scalar(select(User).where(User.id == user_id))


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.scalar(select(User).where(User.username == username))


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(db, username)
    if user is None or not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def create_login_response(user: User) -> dict:
    token = create_access_token(user_id=user.id, username=user.username, role=user.role)
    return {
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": settings.auth_access_token_expire_minutes * 60,
        "user": user,
    }


def seed_default_users(db: Session):
    default_users = [
        {
            "username": "admin",
            "password": "admin123",
            "display_name": "系统管理员",
            "role": "admin",
        },
        {
            "username": "operator",
            "password": "operator123",
            "display_name": "值班员",
            "role": "operator",
        },
        {
            "username": "viewer",
            "password": "viewer123",
            "display_name": "访客只读",
            "role": "viewer",
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
                    is_active=True,
                ),
            )
            continue

        user.display_name = item["display_name"]
        user.role = item["role"]
        user.is_active = True

    db.commit()
