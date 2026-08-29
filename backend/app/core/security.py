import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from app.core.config import settings

def hash_password(plain_password: str) -> str:
    """Turn a plaintext password into a bcrypt hash for storage."""
    pwd_bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plaintext password against a stored hash."""
    pwd_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)

def create_access_token(user_id: int, role: str) -> str:
    """Create a signed JWT carrying the user's id and role."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": str(user_id),   # "subject" — who the token is about
        "role": role,
        "exp": expire,         # expiry — jose checks this automatically
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """Verify a token's signature and expiry. Returns the payload, or None if invalid."""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None