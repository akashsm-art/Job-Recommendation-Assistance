"""
TalentSpark AI — Company Schemas
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from schemas.job import JobResponse


class CompanyCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    founded_year: Optional[int] = None
    tech_stack: Optional[list[str]] = None
    headquarters: Optional[str] = None
    locations: Optional[list[str]] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    culture: Optional[str] = None
    benefits: Optional[list[str]] = None


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    founded_year: Optional[int] = None
    tech_stack: Optional[list[str]] = None
    headquarters: Optional[str] = None
    locations: Optional[list[str]] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    culture: Optional[str] = None
    benefits: Optional[list[str]] = None


class CompanyResponse(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    founded_year: Optional[int] = None
    tech_stack: Optional[list[str]] = None
    headquarters: Optional[str] = None
    locations: Optional[list[str]] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    owner_id: int
    is_verified: bool = False
    is_active: bool = True
    culture: Optional[str] = None
    benefits: Optional[list[str]] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CompanyWithJobsResponse(CompanyResponse):
    jobs: list[JobResponse] = []
