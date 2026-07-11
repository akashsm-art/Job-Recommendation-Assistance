"""
TalentSpark AI — Job Model
Job posting with comprehensive details, skills, and matching metadata.
"""

from database import Base
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, Float,
    ForeignKey, JSON, Enum as SAEnum
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


class JobType(str, enum.Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"


class WorkModeJob(str, enum.Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"


class Job(Base):
    __tablename__ = "jobs"

    # --- Core ---
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=True)
    responsibilities = Column(Text, nullable=True)

    # --- Compensation ---
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    currency = Column(String(10), default="INR")

    # --- Details ---
    job_type = Column(SAEnum(JobType), default=JobType.FULL_TIME)
    work_mode = Column(SAEnum(WorkModeJob), default=WorkModeJob.ONSITE)
    experience_min = Column(Float, nullable=True, default=0)
    experience_max = Column(Float, nullable=True)
    location = Column(String(255), nullable=True)
    is_remote = Column(Boolean, default=False)

    # --- Skills ---
    required_skills = Column(JSON, nullable=True)   # ["Python", "FastAPI", ...]
    preferred_skills = Column(JSON, nullable=True)   # ["Docker", "AWS", ...]

    # --- Education ---
    min_qualification = Column(String(255), nullable=True)

    # --- Company ---
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # --- Status ---
    is_active = Column(Boolean, default=True)
    views_count = Column(Integer, default=0)
    applications_count = Column(Integer, default=0)

    # --- Dates ---
    posted_at = Column(DateTime, default=datetime.utcnow)
    deadline = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --- Additional ---
    tags = Column(JSON, nullable=True)  # ["AI", "Backend", "Startup", ...]
    benefits = Column(JSON, nullable=True)

    # --- Relationships ---
    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
    saved_by = relationship("SavedJob", back_populates="job", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Job(id={self.id}, title='{self.title}')>"
