from sqlalchemy.orm import Session

from app.repositories import user_repo
from app.core.security import hash_password
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token


def register_user(db: Session, data: UserCreate) -> User:
    """Register a new user.

    Rules:
    - email must not already be in use
    - password is hashed before storage
    """
    existing = user_repo.get_user_by_email(db, data.email)
    if existing is not None:
        raise ValueError("Email already registered")

    hashed = hash_password(data.password)

    user = user_repo.create_user(
        db=db,
        email=data.email,
        hashed_password=hashed,
        full_name=data.full_name,
        role="user",  # new signups are always regular users, never admin
    )
    return user

def login_user(db: Session, email: str, password: str) -> str:
    """Verify credentials and return a signed access token.

    Raises ValueError if credentials are invalid.
    """
    user = user_repo.get_user_by_email(db, email)

    # Same error whether email is unknown or password is wrong (prevents enumeration)
    if user is None or not verify_password(password, user.hashed_password):
        raise ValueError("Incorrect email or password")

    if not user.is_active:
        raise ValueError("Account is deactivated")

    return create_access_token(user_id=user.id, role=user.role)