from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.project import ProjectCreate, ProjectRead, AddMemberRequest
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectRead
from app.services import project_service

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create(data: ProjectCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return project_service.create_project(db, user, data.name, data.description)


@router.get("", response_model=list[ProjectRead])
def list_all(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return project_service.list_projects(db, user)


@router.get("/{project_id}", response_model=ProjectRead)
def get_one(project_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        return project_service.get_project(db, user, project_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(project_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        project_service.delete_project(db, user, project_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.post("/{project_id}/members", status_code=status.HTTP_201_CREATED)
def add_member(project_id: int, data: AddMemberRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        project_service.add_member_by_email(db, user, project_id, data.email)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Member added"}


@router.delete("/{project_id}/members/{member_user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member(project_id: int, member_user_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        project_service.remove_member(db, user, project_id, member_user_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))