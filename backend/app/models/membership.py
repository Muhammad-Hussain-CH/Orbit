from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, UniqueConstraint

from app.core.database import Base


class Membership(Base):
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project_role = Column(String, nullable=False, default="member")  # "owner" or "member"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # A user can only be a member of a given project once
    __table_args__ = (UniqueConstraint("user_id", "project_id", name="uq_user_project"),)