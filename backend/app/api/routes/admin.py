from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import require_admin
from app.models.user import User
from app.schemas.user import UserRead
from app.schemas.project import ProjectRead
from app.services import admin_service

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserRead])
def all_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return admin_service.list_all_users(db)


@router.get("/projects", response_model=list[ProjectRead])
def all_projects(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return admin_service.list_all_projects(db)


@router.patch("/users/{user_id}/deactivate", response_model=UserRead)
def deactivate_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    try:
        return admin_service.set_user_active(db, admin, user_id, is_active=False)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/users/{user_id}/activate", response_model=UserRead)
def activate_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    try:
        return admin_service.set_user_active(db, admin, user_id, is_active=True)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))