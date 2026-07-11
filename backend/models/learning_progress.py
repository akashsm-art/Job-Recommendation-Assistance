"""
TalentSpark AI — LearningProgress Model
Track user progress through courses.
"""

from database import Base
from sqlalchemy import (
    Column, Integer, Float, DateTime, ForeignKey,
    Enum as SAEnum, UniqueConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


class LearningStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PAUSED = "paused"


class LearningProgress(Base):
    __tablename__ = "learning_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    status = Column(SAEnum(LearningStatus), default=LearningStatus.NOT_STARTED)
    progress_pct = Column(Float, default=0)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --- Unique: one progress record per user-course pair ---
    __table_args__ = (UniqueConstraint("user_id", "course_id", name="uq_user_course_progress"),)

    # --- Relationships ---
    user = relationship("User", back_populates="learning_progress")
    course = relationship("Course", back_populates="learning_progress")

    def __repr__(self):
        return f"<LearningProgress(user_id={self.user_id}, course_id={self.course_id}, progress={self.progress_pct}%)>"
