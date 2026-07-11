"""
TalentSpark AI — Pydantic Schemas for Phase 2 Advanced AI Features
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# --- Salary Prediction ---
class SalaryPredictionRequest(BaseModel):
    role: str
    experience_years: float
    skills: List[str]
    location: Optional[str] = None
    current_ctc: Optional[float] = None
    education: Optional[str] = None
    use_llm: bool = False


class SalaryPredictionResponse(BaseModel):
    predicted_min_lpa: float
    predicted_max_lpa: float
    recommended_ctc_lpa: float
    confidence_pct: int
    currency: str = "INR"
    hike_percentage: Optional[float] = None
    factors: List[str] = []
    premium_skills: List[str] = []
    market_trend: str
    comparable_roles: List[str] = []
    reasoning: Optional[str] = None
    negotiation_tips: Optional[List[str]] = None
    market_insight: Optional[str] = None


# --- Career Roadmap ---
class CareerRoadmapRequest(BaseModel):
    target_role: str
    use_llm: bool = False


class RoadmapPhase(BaseModel):
    phase: int
    title: str
    duration: str
    skills: List[str]
    skills_known: List[str] = []
    skills_to_learn: List[str] = []
    resources: List[str]
    projects: List[str]
    milestone: str
    completion_pct: float
    status: str
    adjusted_duration: Optional[str] = None


class CareerRoadmapResponse(BaseModel):
    title: str
    estimated_duration: str
    overall_readiness: float
    skills_gap_count: Optional[int] = None
    current_skills_count: Optional[int] = None
    phases: List[RoadmapPhase]
    tips: List[str]


# --- Resume Rewriting & Cover Letters ---
class ResumeRewriteRequest(BaseModel):
    resume_text: str
    target_role: str
    job_description: Optional[str] = None


class ResumeRewriteResponse(BaseModel):
    professional_summary: str
    key_highlights: List[str]
    optimized_skills: Dict[str, List[str]]
    experience_bullets: List[str]
    keywords_added: List[str]
    ats_tips: List[str]
    before_after: List[Dict[str, str]] = []
    overall_improvement: str


class CoverLetterRequest(BaseModel):
    target_role: str
    company_name: str
    job_description: Optional[str] = None
    tone: str = "professional"  # professional, creative, casual


class CoverLetterResponse(BaseModel):
    cover_letter: str
    subject_line: str
    key_selling_points: List[str]
    personalization_tips: List[str]
    word_count: int


# --- Interview Prep ---
class InterviewPrepRequest(BaseModel):
    role: str
    difficulty: str = "Medium"
    categories: List[str] = ["mcq", "coding", "system_design", "hr", "behavioral"]
    num_questions: int = 10
    company: Optional[str] = None


class InterviewPrepResponse(BaseModel):
    role: str
    difficulty: str
    company: Optional[str] = None
    sections: Dict[str, Any]
    tips: List[str]


class MockInterviewRound(BaseModel):
    round: int
    title: str
    duration: str
    type: str
    questions: List[Any]
    scoring: Dict[str, Any]


class MockInterviewResponse(BaseModel):
    role: str
    difficulty: str
    total_rounds: int
    estimated_duration: str
    rounds: List[MockInterviewRound]


class InterviewAnswerEvaluationRequest(BaseModel):
    question: str
    answer: str
    role: str


class InterviewAnswerEvaluationResponse(BaseModel):
    score: int
    max_score: int = 100
    feedback: str
    strengths: List[str]
    improvements: List[str]
    ideal_answer_outline: str
    communication_score: int
    technical_score: int
    confidence_score: int


# --- Company Fit ---
class CompanyFitRequest(BaseModel):
    company_id: int
    use_llm: bool = False


class CompanyFitResponse(BaseModel):
    scores: Dict[str, float]
    recommendation: str
    matching_tech: List[str]
    missing_tech: List[str]
    insights: List[str]
    overall_fit_pct: Optional[float] = None
    dimensions: Optional[Dict[str, Any]] = None
    pros: Optional[List[str]] = None
    cons: Optional[List[str]] = None
    questions_to_ask: Optional[List[str]] = None


# --- Skill Trends ---
class SkillTrendRequest(BaseModel):
    skills: Optional[List[str]] = None


class SkillTrendInfo(BaseModel):
    demand: str
    trend: str
    growth_pct: float
    avg_salary_boost_pct: Optional[float] = None
    category: Optional[str] = None


class SkillTrendResponse(BaseModel):
    skills: Optional[Dict[str, SkillTrendInfo]] = None
    categories: Optional[Dict[str, List[Dict[str, Any]]]] = None
    updated: str


class JobMarketOverviewResponse(BaseModel):
    trends: Dict[str, Any]
    top_growing_skills: List[Dict[str, Any]]
    hot_roles: List[Dict[str, Any]]
    insights: List[str]
    updated: str


class UserSkillValueAnalysisResponse(BaseModel):
    trending_skills: List[Dict[str, Any]]
    stable_skills: List[Dict[str, Any]]
    declining_skills: List[Dict[str, Any]]
    untracked_skills: List[str]
    estimated_salary_boost_pct: float
    market_readiness: Dict[str, Any]
    recommendations: List[str]


# --- Resume Builder ---
class ResumeBuildRequest(BaseModel):
    template: str = "modern"
    target_role: Optional[str] = None


class ResumeBuildResponse(BaseModel):
    template: Dict[str, str]
    generated_at: str
    sections: Dict[str, Any]


class ResumeHtmlResponse(BaseModel):
    html: str


# --- Recruiter AI ---
class RankCandidatesRequest(BaseModel):
    job_id: int


class CandidateRankInfo(BaseModel):
    user_id: int
    name: str
    email: str
    match_score: float
    technical_match: float
    experience_match: float
    education_match: float
    matching_skills: List[str]
    missing_skills: List[str]
    rank_reason: str
    rank: int
    tier: str


class CandidateRankingResponse(BaseModel):
    ranked_candidates: List[CandidateRankInfo]


class DuplicateDetectionRequest(BaseModel):
    resume_text_1: str
    resume_text_2: str


class DuplicateDetectionResponse(BaseModel):
    similarity_score: float
    cosine_similarity: float
    text_overlap_pct: float
    is_duplicate: bool
    verdict: str


class ResumeAuthenticityRequest(BaseModel):
    resume_text: str


class ResumeAuthenticityResponse(BaseModel):
    authenticity_score: int
    verdict: str
    flags: List[str]
    word_count: int
    has_contact_info: bool
    has_verifiable_links: bool
    recommendations: List[str]


class RecruiterPoolSummaryResponse(BaseModel):
    summary: str
    stats: Dict[str, Any]
    top_skills_in_pool: List[Dict[str, Any]]
    recommendation: str
