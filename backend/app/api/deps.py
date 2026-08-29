from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.repositories import user_repo
from app.models.user import User

# Tells FastAPI to look for a "Authorization: Bearer <token>" header.
# tokenUrl points at the login route (used by the /docs UI to log in).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Verify the token, load the user, or reject with 401."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_error

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_error

    user = user_repo.get_user_by_id(db, int(user_id))
    if user is None or not user.is_active:
        raise credentials_error

    return user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Allow only admin users. Rejects everyone else with 403."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user