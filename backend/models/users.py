"""
TalentSpark AI — User Model
Comprehensive user model supporting Candidate, Recruiter, and Admin roles.
"""

from database import Base
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Date, DateTime, Float,
    Enum as SAEnum, JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


class UserRole(str, enum.Enum):
    CANDIDATE = "candidate"
    RECRUITER = "recruiter"
    ADMIN = "admin"


class WorkMode(str, enum.Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class User(Base):
    __tablename__ = "users"

    # --- Core ---
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.CANDIDATE)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # --- Profile ---
    full_name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    dob = Column(Date, nullable=True)
    gender = Column(SAEnum(Gender), nullable=True)
    photo_url = Column(String(500), nullable=True)
    nationality = Column(String(100), nullable=True)
    languages_known = Column(JSON, nullable=True)  # ["English", "Hindi", ...]

    # --- Address ---
    current_address = Column(Text, nullable=True)
    permanent_address = Column(Text, nullable=True)

    # --- Social / Links ---
    linkedin = Column(String(500), nullable=True)
    github = Column(String(500), nullable=True)
    portfolio = Column(String(500), nullable=True)
    leetcode = Column(String(500), nullable=True)
    hackerrank = Column(String(500), nullable=True)
    codechef = Column(String(500), nullable=True)
    codeforces = Column(String(500), nullable=True)

    # --- Professional (Candidate) ---
    current_company = Column(String(255), nullable=True)
    current_ctc = Column(Float, nullable=True)
    expected_ctc = Column(Float, nullable=True)
    experience_years = Column(Float, nullable=True, default=0)
    notice_period = Column(String(50), nullable=True)  # "Immediate", "15 days", "1 month", etc.
    availability = Column(String(100), nullable=True)

    # --- Preferences ---
    preferred_role = Column(String(255), nullable=True)
    preferred_location = Column(String(255), nullable=True)
    expected_salary = Column(Float, nullable=True)
    work_mode = Column(SAEnum(WorkMode), nullable=True)

    # --- Education (Summary) ---
    highest_qualification = Column(String(255), nullable=True)
    university = Column(String(255), nullable=True)
    cgpa = Column(Float, nullable=True)

    # --- Career ---
    career_objective = Column(Text, nullable=True)
    resume_url = Column(String(500), nullable=True)
    resume_text = Column(Text, nullable=True)  # Parsed resume content

    # --- Technical Skills (JSON arrays) ---
    technical_skills = Column(JSON, nullable=True)
    soft_skills = Column(JSON, nullable=True)
    programming_languages = Column(JSON, nullable=True)
    frameworks = Column(JSON, nullable=True)
    databases_known = Column(JSON, nullable=True)
    cloud_skills = Column(JSON, nullable=True)
    ai_skills = Column(JSON, nullable=True)

    # --- Auth ---
    refresh_token = Column(String(500), nullable=True)
    reset_token = Column(String(500), nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)
    google_id = Column(String(255), nullable=True, unique=True)

    # --- Profile Completion ---
    profile_completion = Column(Integer, default=0)

    # --- Timestamps ---
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --- Relationships ---
    skills = relationship("Skill", back_populates="user", cascade="all, delete-orphan")
    education_records = relationship("Education", back_populates="user", cascade="all, delete-orphan")
    experience_records = relationship("Experience", back_populates="user", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="user", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")
    saved_jobs = relationship("SavedJob", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    chat_histories = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")
    resume_scores = relationship("ResumeScore", back_populates="user", cascade="all, delete-orphan")
    learning_progress = relationship("LearningProgress", back_populates="user", cascade="all, delete-orphan")
    companies = relationship("Company", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
