from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    """Return the user with this email, or None if not found."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Return the user with this id, or None if not found."""
    return db.query(User).filter(User.id == user_id).first()


def create_user(
    db: Session,
    email: str,
    hashed_password: str,
    full_name: str,
    role: str = "user",
) -> User:
    """Insert a new user row and return it."""
    user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db: Session) -> list[User]:
    """Every user in the system — admin use only."""
    return db.query(User).order_by(User.id).all()


def set_user_active(db: Session, user: User, is_active: bool) -> User:
    """Activate or deactivate a user account."""
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user