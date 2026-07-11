"""
TalentSpark AI — Course Schemas
"""

from pydantic import BaseModel
from typing import Optional


class CourseResponse(BaseModel):
    id: int
    title: str
    provider: str
    url: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    duration: Optional[str] = None
    difficulty: Optional[str] = None
    skill: Optional[str] = None
    category: Optional[str] = None
    is_free: bool = False
    has_certificate: bool = True
    price: Optional[str] = None
    estimated_completion: Optional[str] = None

    class Config:
        from_attributes = True


class CourseRecommendation(BaseModel):
    skill: str
    courses: list[CourseResponse] = []
    learning_path: Optional[str] = None
