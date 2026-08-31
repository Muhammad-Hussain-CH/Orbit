from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func

from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False, default="todo")  # todo, in_progress, done
    created_at = Column(DateTime(timezone=True), server_default=func.now())