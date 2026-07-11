"""
TalentSpark AI — Application Model
Tracks job applications with status pipeline.
"""

from database import Base
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey,
    Enum as SAEnum, Float
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


class ApplicationStatus(str, enum.Enum):
    APPLIED = "applied"
    UNDER_REVIEW = "under_review"
    SHORTLISTED = "shortlisted"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEWED = "interviewed"
    OFFERED = "offered"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    status = Column(SAEnum(ApplicationStatus), default=ApplicationStatus.APPLIED)
    cover_letter = Column(Text, nullable=True)
    resume_snapshot = Column(Text, nullable=True)  # Resume text at time of application
    match_score = Column(Float, nullable=True)  # AI-calculated match score
    match_details = Column(Text, nullable=True)  # AI explanation

    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --- Relationships ---
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")

    def __repr__(self):
        return f"<Application(user_id={self.user_id}, job_id={self.job_id}, status='{self.status}')>"
