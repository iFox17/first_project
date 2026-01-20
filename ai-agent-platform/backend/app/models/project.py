from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from .base import BaseModel


class Project(BaseModel):
    __tablename__ = "projects"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(String(50), nullable=False)  # mobile_game, app, web_service
    platform = Column(String(50), nullable=True)  # yandex_games, app_store, play_store, web
    status = Column(String(30), default="idea")  # idea, planning, in_progress, completed, archived
    metadata = Column(JSONB, default={})

    # Relationships
    user = relationship("User", back_populates="projects")
    conversations = relationship("Conversation", back_populates="project")
    stages = relationship("PlanStage", back_populates="project", cascade="all, delete-orphan", order_by="PlanStage.order_index")


class PlanStage(BaseModel):
    __tablename__ = "plan_stages"

    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, nullable=False)
    status = Column(String(30), default="pending")  # pending, in_progress, completed
    estimated_hours = Column(Integer, nullable=True)

    # Relationships
    project = relationship("Project", back_populates="stages")
    tasks = relationship("PlanTask", back_populates="stage", cascade="all, delete-orphan", order_by="PlanTask.order_index")


class PlanTask(BaseModel):
    __tablename__ = "plan_tasks"

    stage_id = Column(UUID(as_uuid=True), ForeignKey("plan_stages.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, nullable=False)
    status = Column(String(30), default="pending")  # pending, in_progress, completed
    assigned_agent = Column(String(50), nullable=True)  # marketer, developer, pm
    estimated_hours = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    stage = relationship("PlanStage", back_populates="tasks")
