from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.membership import Membership


def create_project(db: Session, name: str, description: str | None) -> Project:
    project = Project(name=name, description=description)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_project_by_id(db: Session, project_id: int) -> Project | None:
    return db.query(Project).filter(Project.id == project_id).first()


def get_projects_for_user(db: Session, user_id: int) -> list[Project]:
    """All projects this user is a member of (joins through memberships)."""
    return (
        db.query(Project)
        .join(Membership, Membership.project_id == Project.id)
        .filter(Membership.user_id == user_id)
        .all()
    )


def add_member(db: Session, project_id: int, user_id: int, project_role: str) -> Membership:
    membership = Membership(
        project_id=project_id, user_id=user_id, project_role=project_role
    )
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


def get_membership(db: Session, project_id: int, user_id: int) -> Membership | None:
    """The membership linking this user to this project, or None."""
    return (
        db.query(Membership)
        .filter(Membership.project_id == project_id, Membership.user_id == user_id)
        .first()
    )


def update_project(db: Session, project: Project, name: str | None, description: str | None) -> Project:
    if name is not None:
        project.name = name
    if description is not None:
        project.description = description
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project: Project) -> None:
    db.delete(project)
    db.commit()

def get_all_projects(db: Session) -> list[Project]:
    """Every project in the system — admin use only."""
    return db.query(Project).order_by(Project.id).all()