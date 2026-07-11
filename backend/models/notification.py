"""
TalentSpark AI — Notification Model
In-app notifications for users.
"""

from database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


class NotificationType(str, enum.Enum):
    JOB_ALERT = "job_alert"
    APPLICATION_STATUS = "application_status"
    INTERVIEW_SCHEDULE = "interview_schedule"
    COURSE_REMINDER = "course_reminder"
    WEEKLY_REPORT = "weekly_report"
    SYSTEM = "system"
    AI_INSIGHT = "ai_insight"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(SAEnum(NotificationType), default=NotificationType.SYSTEM)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=True)
    is_read = Column(Boolean, default=False)
    link = Column(String(500), nullable=True)  # Deep link to relevant page
    created_at = Column(DateTime, default=datetime.utcnow)

    # --- Relationship ---
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(title='{self.title}', type='{self.type}')>"
