"""
TalentSpark AI — Company Model
Company profile for recruiters with full details.
"""

from database import Base
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime


class Company(Base):
    __tablename__ = "companies"

    # --- Core ---
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True)
    phone = Column(String(20), nullable=True)
    website = Column(String(500), nullable=True)
    logo_url = Column(String(500), nullable=True)

    # --- Details ---
    description = Column(Text, nullable=True)
    industry = Column(String(255), nullable=True)
    company_size = Column(String(50), nullable=True)  # "1-10", "11-50", "51-200", etc.
    founded_year = Column(Integer, nullable=True)
    tech_stack = Column(JSON, nullable=True)  # ["Python", "React", ...]

    # --- Location ---
    headquarters = Column(String(255), nullable=True)
    locations = Column(JSON, nullable=True)  # ["Bangalore", "Mumbai", ...]

    # --- Social ---
    linkedin = Column(String(500), nullable=True)
    twitter = Column(String(500), nullable=True)
    glassdoor_url = Column(String(500), nullable=True)

    # --- Owner (Recruiter) ---
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # --- Status ---
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # --- Culture & Benefits ---
    culture = Column(Text, nullable=True)
    benefits = Column(JSON, nullable=True)  # ["Health Insurance", "Remote", ...]
    perks = Column(JSON, nullable=True)

    # --- Timestamps ---
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --- Relationships ---
    owner = relationship("User", back_populates="companies")
    jobs = relationship("Job", back_populates="company", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}')>"
