from sqlalchemy.orm import Session
from app.repositories import user_repo
from app.repositories import project_repo
from app.models.project import Project
from app.models.user import User


def create_project(db: Session, user: User, name: str, description: str | None) -> Project:
    """Create a project and make the creator its owner."""
    project = project_repo.create_project(db, name=name, description=description)
    project_repo.add_member(db, project_id=project.id, user_id=user.id, project_role="owner")
    return project


def list_projects(db: Session, user: User) -> list[Project]:
    """Only the projects this user belongs to."""
    return project_repo.get_projects_for_user(db, user.id)


def get_project(db: Session, user: User, project_id: int) -> Project:
    """Fetch a project, but only if the user is a member."""
    project = project_repo.get_project_by_id(db, project_id)
    if project is None:
        raise LookupError("Project not found")

    membership = project_repo.get_membership(db, project_id, user.id)
    if membership is None:
        raise PermissionError("You are not a member of this project")

    return project


def delete_project(db: Session, user: User, project_id: int) -> None:
    """Delete a project — only the owner may do this."""
    project = project_repo.get_project_by_id(db, project_id)
    if project is None:
        raise LookupError("Project not found")

    membership = project_repo.get_membership(db, project_id, user.id)
    if membership is None:
        raise PermissionError("You are not a member of this project")
    if membership.project_role != "owner":
        raise PermissionError("Only the project owner can delete it")

    project_repo.delete_project(db, project)


def _require_owner(db: Session, user: User, project_id: int):
    """Shared check: the project exists and the user owns it."""
    project = project_repo.get_project_by_id(db, project_id)
    if project is None:
        raise LookupError("Project not found")
    membership = project_repo.get_membership(db, project_id, user.id)
    if membership is None or membership.project_role != "owner":
        raise PermissionError("Only the project owner can manage members")
    return project


def add_member_by_email(db: Session, user: User, project_id: int, email: str) -> None:
    """Owner adds another user (by email) to the project as a member."""
    _require_owner(db, user, project_id)

    new_member = user_repo.get_user_by_email(db, email)
    if new_member is None:
        raise LookupError("No user with that email")

    existing = project_repo.get_membership(db, project_id, new_member.id)
    if existing is not None:
        raise ValueError("User is already a member")

    project_repo.add_member(db, project_id=project_id, user_id=new_member.id, project_role="member")


def remove_member(db: Session, user: User, project_id: int, member_user_id: int) -> None:
    """Owner removes a member from the project."""
    _require_owner(db, user, project_id)

    membership = project_repo.get_membership(db, project_id, member_user_id)
    if membership is None:
        raise LookupError("That user is not a member")
    if membership.project_role == "owner":
        raise ValueError("The owner cannot be removed")

    db.delete(membership)
    db.commit()