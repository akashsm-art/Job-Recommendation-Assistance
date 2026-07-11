"""
TalentSpark AI — Application Schemas
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ApplicationCreate(BaseModel):
    job_id: int
    cover_letter: Optional[str] = None


class ApplicationUpdate(BaseModel):
    status: str  # "under_review", "shortlisted", "rejected", etc.


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    status: str
    cover_letter: Optional[str] = None
    match_score: Optional[float] = None
    match_details: Optional[str] = None
    applied_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
