from sqlalchemy.orm import Session

from app.models.task import Task


def create_task(db: Session, project_id: int, title: str, description: str | None) -> Task:
    task = Task(project_id=project_id, title=title, description=description)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks_for_project(db: Session, project_id: int) -> list[Task]:
    return db.query(Task).filter(Task.project_id == project_id).order_by(Task.id).all()


def get_task_by_id(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(db: Session, task: Task, title, description, status) -> Task:
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if status is not None:
        task.status = status
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()