from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.services import task_service

router = APIRouter(tags=["tasks"])


@router.post("/projects/{project_id}/tasks", response_model=TaskRead, status_code=201)
def create(project_id: int, data: TaskCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        return task_service.create_task(db, user, project_id, data.title, data.description)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/projects/{project_id}/tasks", response_model=list[TaskRead])
def list_all(project_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        return task_service.list_tasks(db, user, project_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.patch("/tasks/{task_id}", response_model=TaskRead)
def update(task_id: int, data: TaskUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        return task_service.update_task(db, user, task_id, data.title, data.description, data.status)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/tasks/{task_id}", status_code=204)
def delete(task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        task_service.delete_task(db, user, task_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))