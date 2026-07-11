"""
TalentSpark AI — Recommendation Schemas
"""

from pydantic import BaseModel
from typing import Optional


class JobMatchScore(BaseModel):
    overall_match: float
    technical_match: float
    experience_match: float
    location_match: float
    salary_match: float
    education_match: float
    soft_skills_match: float
    culture_match: float


class JobRecommendation(BaseModel):
    job_id: int
    title: str
    company_name: str
    location: Optional[str] = None
    salary_range: Optional[str] = None
    match_score: float
    match_details: JobMatchScore
    matching_skills: list[str] = []
    missing_skills: list[str] = []
    reason: str  # AI-generated explanation


class SkillGapAnalysis(BaseModel):
    job_id: int
    job_title: str
    compatibility_pct: float
    matching_skills: list[str] = []
    missing_skills: list[str] = []
    recommended_courses: list[dict] = []
    roadmap: Optional[str] = None
    can_apply: bool = True
    message: str


class RAGSearchRequest(BaseModel):
    question: str


class RAGSearchResponse(BaseModel):
    question: str
    answer: str


class EmbedJobsResponse(BaseModel):
    message: str
    jobs_embedded: int
