from sqlalchemy.orm import Session

from app.repositories import user_repo
from app.core.security import hash_password
from app.schemas.user import UserCreate
from app.models.user import User


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