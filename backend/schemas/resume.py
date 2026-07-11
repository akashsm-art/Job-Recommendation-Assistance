"""
TalentSpark AI — Resume & ATS Schemas
"""

from pydantic import BaseModel
from typing import Optional


class ResumeParseResponse(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: list[str] = []
    education: list[dict] = []
    experience: list[dict] = []
    projects: list[dict] = []
    certifications: list[str] = []
    links: list[str] = []
    languages: list[str] = []
    summary: Optional[str] = None


class ATSScoreResponse(BaseModel):
    ats_score: float
    formatting_score: float
    keyword_score: float
    grammar_score: float
    projects_score: float
    experience_score: float
    skills_score: float
    education_score: float
    overall_score: float
    suggestions: list[str] = []
    missing_skills: list[str] = []
    missing_keywords: list[str] = []
    strengths: list[str] = []
    weaknesses: list[str] = []
    heatmap: dict = {}


class ResumeUploadResponse(BaseModel):
    message: str
    parsed_data: Optional[ResumeParseResponse] = None
    ats_scores: Optional[ATSScoreResponse] = None
    resume_url: Optional[str] = None
