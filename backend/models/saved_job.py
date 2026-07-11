"""
TalentSpark AI — SavedJob Model
Bookmarked/saved jobs for candidates.
"""

from database import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime


class SavedJob(Base):
    __tablename__ = "saved_jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    saved_at = Column(DateTime, default=datetime.utcnow)

    # --- Unique constraint: user can save a job only once ---
    __table_args__ = (UniqueConstraint("user_id", "job_id", name="uq_user_saved_job"),)

    # --- Relationships ---
    user = relationship("User", back_populates="saved_jobs")
    job = relationship("Job", back_populates="saved_by")

    def __repr__(self):
        return f"<SavedJob(user_id={self.user_id}, job_id={self.job_id})>"
