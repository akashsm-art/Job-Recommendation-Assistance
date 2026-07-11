"""
TalentSpark AI — Job Schemas
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class JobCreate(BaseModel):
    title: str
    description: str
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: str = "INR"
    job_type: str = "full_time"
    work_mode: str = "onsite"
    experience_min: Optional[float] = None
    experience_max: Optional[float] = None
    location: Optional[str] = None
    is_remote: bool = False
    required_skills: Optional[list[str]] = None
    preferred_skills: Optional[list[str]] = None
    min_qualification: Optional[str] = None
    company_id: int
    deadline: Optional[datetime] = None
    tags: Optional[list[str]] = None
    benefits: Optional[list[str]] = None


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: Optional[str] = None
    job_type: Optional[str] = None
    work_mode: Optional[str] = None
    experience_min: Optional[float] = None
    experience_max: Optional[float] = None
    location: Optional[str] = None
    is_remote: Optional[bool] = None
    required_skills: Optional[list[str]] = None
    preferred_skills: Optional[list[str]] = None
    min_qualification: Optional[str] = None
    is_active: Optional[bool] = None
    deadline: Optional[datetime] = None
    tags: Optional[list[str]] = None
    benefits: Optional[list[str]] = None


class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: str = "INR"
    job_type: Optional[str] = None
    work_mode: Optional[str] = None
    experience_min: Optional[float] = None
    experience_max: Optional[float] = None
    location: Optional[str] = None
    is_remote: bool = False
    required_skills: Optional[list[str]] = None
    preferred_skills: Optional[list[str]] = None
    min_qualification: Optional[str] = None
    company_id: int
    is_active: bool = True
    views_count: int = 0
    applications_count: int = 0
    tags: Optional[list[str]] = None
    benefits: Optional[list[str]] = None
    posted_at: Optional[datetime] = None
    deadline: Optional[datetime] = None

    class Config:
        from_attributes = True


class JobSearchFilters(BaseModel):
    query: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    work_mode: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    experience_min: Optional[float] = None
    experience_max: Optional[float] = None
    skills: Optional[list[str]] = None
    company_id: Optional[int] = None
    is_remote: Optional[bool] = None
    page: int = 1
    page_size: int = 20
