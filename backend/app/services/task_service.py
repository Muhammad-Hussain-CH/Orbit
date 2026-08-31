from sqlalchemy.orm import Session

from app.repositories import task_repo
from app.services import project_service
from app.models.task import Task
from app.models.user import User


def create_task(db: Session, user: User, project_id: int, title: str, description: str | None) -> Task:
    # reuses the project membership check — raises if user can't access the project
    project_service.get_project(db, user, project_id)
    return task_repo.create_task(db, project_id, title, description)


def list_tasks(db: Session, user: User, project_id: int) -> list[Task]:
    project_service.get_project(db, user, project_id)
    return task_repo.get_tasks_for_project(db, project_id)


def _get_task_in_accessible_project(db: Session, user: User, task_id: int) -> Task:
    task = task_repo.get_task_by_id(db, task_id)
    if task is None:
        raise LookupError("Task not found")
    # membership check via the task's project
    project_service.get_project(db, user, task.project_id)
    return task


def update_task(db: Session, user: User, task_id: int, title, description, status) -> Task:
    task = _get_task_in_accessible_project(db, user, task_id)
    return task_repo.update_task(db, task, title, description, status)


def delete_task(db: Session, user: User, task_id: int) -> None:
    task = _get_task_in_accessible_project(db, user, task_id)
    task_repo.delete_task(db, task)