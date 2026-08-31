from sqlalchemy.orm import Session

from app.repositories import user_repo, project_repo
from app.models.user import User
from app.models.project import Project


def list_all_users(db: Session) -> list[User]:
    return user_repo.get_all_users(db)


def list_all_projects(db: Session) -> list[Project]:
    return project_repo.get_all_projects(db)


def set_user_active(db: Session, admin: User, target_user_id: int, is_active: bool) -> User:
    if admin.id == target_user_id:
        raise ValueError("You cannot change your own active status")

    target = user_repo.get_user_by_id(db, target_user_id)
    if target is None:
        raise LookupError("User not found")

    return user_repo.set_user_active(db, target, is_active)