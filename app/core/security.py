import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

password_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return password_context.hash(password)


def _verify_legacy_pbkdf2(password: str, password_hash: str) -> bool:
    # 兼容旧格式: pbkdf2_sha256$120000$salt$hex_digest
    try:
        algorithm, iterations_text, salt_text, digest_hex = password_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        iterations = int(iterations_text)
    except ValueError:
        return False

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt_text.encode("utf-8"),
        iterations,
    )
    return hmac.compare_digest(digest.hex(), digest_hex)


def verify_password(password: str, password_hash: str) -> bool:
    if not password_hash:
        return False
    if password_hash.startswith("pbkdf2_sha256$"):
        return _verify_legacy_pbkdf2(password, password_hash)
    return password_context.verify(password, password_hash)


def create_access_token(*, user_id: int, username: str, role: str) -> tuple[str, str, datetime]:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=settings.auth_access_token_expire_minutes)
    jti = uuid4().hex
    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "jti": jti,
        "exp": int(expires_at.timestamp()),
        "iat": int(now.timestamp()),
        "type": "access",
    }
    token = jwt.encode(payload, settings.auth_secret_key, algorithm=settings.auth_algorithm)
    return token, jti, expires_at.replace(tzinfo=None)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.auth_secret_key, algorithms=[settings.auth_algorithm])
    except JWTError as exc:
        raise ValueError("invalid token") from exc
