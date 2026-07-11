"""
TalentSpark AI — RAG Router
RAG search, embed jobs, ATS analysis, recommendations, skill gap, course recommendations.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional

from database import get_db
from models.users import User
from schemas.recommendation import RAGSearchRequest, RAGSearchResponse, EmbedJobsResponse
from utils.oauth2 import get_current_user, role_required

router = APIRouter(prefix="/rag", tags=["AI & RAG"])


# --- Request Schemas ---

class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    job_description: Optional[str] = None


class InterviewPrepRequest(BaseModel):
    role: str
    difficulty: str = "Medium"
    focus_areas: Optional[str] = None
    num_questions: int = 10


class LearningPathRequest(BaseModel):
    target_role: Optional[str] = None


class CourseRecommendRequest(BaseModel):
    missing_skills: list[str]


# --- Endpoints ---

@router.post("/search", response_model=RAGSearchResponse)
def rag_search(request: RAGSearchRequest):
    """RAG-based semantic job search."""
    try:
        from services.rag import rag_job_search
        answer = rag_job_search(request.question)
        return RAGSearchResponse(question=request.question, answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/embed-jobs", response_model=EmbedJobsResponse)
async def embed_jobs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required(["admin"])),
):
    """Embed all active jobs into ChromaDB vector store (admin only)."""
    try:
        from services.embeddings import embed_all_jobs
        count = await embed_all_jobs(db)
        return EmbedJobsResponse(
            message=f"Successfully embedded {count} jobs into ChromaDB.",
            jobs_embedded=count,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-resume")
async def analyze_resume(
    request: ResumeAnalysisRequest,
    current_user: User = Depends(get_current_user),
):
    """Comprehensive ATS resume analysis."""
    try:
        from services.ats import analyze_resume_ats
        analysis = analyze_resume_ats(request.resume_text, request.job_description)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommend-jobs")
async def recommend_jobs(
    current_user: User = Depends(role_required(["candidate"])),
    db: AsyncSession = Depends(get_db),
):
    """Get AI-powered job recommendations based on user profile and resume."""
    try:
        from services.recommender import recommend_jobs_for_user

        # Build user data dict
        user_data = {
            "technical_skills": current_user.technical_skills or [],
            "soft_skills": current_user.soft_skills or [],
            "programming_languages": current_user.programming_languages or [],
            "frameworks": current_user.frameworks or [],
            "databases_known": current_user.databases_known or [],
            "cloud_skills": current_user.cloud_skills or [],
            "ai_skills": current_user.ai_skills or [],
            "skill_records": [s.name for s in (current_user.skills or [])],
            "experience_years": current_user.experience_years or 0,
            "preferred_role": current_user.preferred_role,
            "preferred_location": current_user.preferred_location,
            "expected_salary": current_user.expected_salary,
            "work_mode": current_user.work_mode.value if current_user.work_mode else None,
            "highest_qualification": current_user.highest_qualification,
            "career_objective": current_user.career_objective,
        }

        recommendations = recommend_jobs_for_user(user_data)
        return {"recommendations": recommendations, "count": len(recommendations)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommend-courses")
async def recommend_courses(
    request: CourseRecommendRequest,
    current_user: User = Depends(get_current_user),
):
    """Get course recommendations for missing skills."""
    try:
        from services.course_recommender import recommend_courses_for_skills
        recommendations = recommend_courses_for_skills(request.missing_skills)
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/learning-path")
async def generate_learning_path_endpoint(
    request: LearningPathRequest,
    current_user: User = Depends(get_current_user),
):
    """Generate a personalized learning roadmap."""
    try:
        from services.course_recommender import generate_learning_path

        user_skills = []
        for key in ["technical_skills", "programming_languages", "frameworks"]:
            user_skills.extend(getattr(current_user, key) or [])
        user_skills.extend([s.name for s in (current_user.skills or [])])

        path = generate_learning_path(
            user_skills,
            request.target_role or current_user.preferred_role or "Full Stack Developer"
        )
        return {"learning_path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/interview-prep")
async def interview_preparation(
    request: InterviewPrepRequest,
    current_user: User = Depends(get_current_user),
):
    """Generate interview preparation questions."""
    try:
        from services.rag import generate_interview_questions
        questions = generate_interview_questions(
            request.role, request.difficulty, request.focus_areas, request.num_questions
        )
        return {"role": request.role, "difficulty": request.difficulty, "questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/resume-review")
async def review_resume(
    request: ResumeAnalysisRequest,
    current_user: User = Depends(get_current_user),
):
    """AI-powered resume review with actionable feedback."""
    try:
        from services.rag import rag_resume_review
        review = rag_resume_review(request.resume_text)
        return {"review": review}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard-stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get dashboard statistics for the current user."""
    from sqlalchemy import func
    from models.application import Application
    from models.saved_job import SavedJob
    from models.resume_score import ResumeScore
    from models.job import Job

    stats = {}

    if current_user.role.value == "candidate":
        # Application stats
        app_count = await db.execute(
            select(func.count(Application.id)).filter(Application.user_id == current_user.id)
        )
        stats["total_applications"] = app_count.scalar() or 0

        # Saved jobs
        saved_count = await db.execute(
            select(func.count(SavedJob.id)).filter(SavedJob.user_id == current_user.id)
        )
        stats["saved_jobs"] = saved_count.scalar() or 0

        # Latest resume score
        latest_score = await db.execute(
            select(ResumeScore)
            .filter(ResumeScore.user_id == current_user.id)
            .order_by(ResumeScore.created_at.desc())
            .limit(1)
        )
        score = latest_score.scalars().first()
        stats["resume_score"] = score.overall_score if score else None
        stats["ats_score"] = score.ats_score if score else None

        stats["profile_completion"] = current_user.profile_completion or 0

    elif current_user.role.value in ["recruiter", "admin"]:
        from models.company import Company

        # Company count
        company_count = await db.execute(
            select(func.count(Company.id)).filter(Company.owner_id == current_user.id)
        )
        stats["total_companies"] = company_count.scalar() or 0

        # Job count
        job_count = await db.execute(
            select(func.count(Job.id))
            .join(Company, Job.company_id == Company.id)
            .filter(Company.owner_id == current_user.id)
        )
        stats["total_jobs"] = job_count.scalar() or 0

        # Application count for their jobs
        app_count = await db.execute(
            select(func.count(Application.id))
            .join(Job, Application.job_id == Job.id)
            .join(Company, Job.company_id == Company.id)
            .filter(Company.owner_id == current_user.id)
        )
        stats["total_applications"] = app_count.scalar() or 0

    if current_user.role.value == "admin":
        total_users = await db.execute(select(func.count(User.id)))
        total_jobs = await db.execute(select(func.count(Job.id)))
        total_companies = await db.execute(
            select(func.count(Company.id))
        )
        stats["platform_users"] = total_users.scalar() or 0
        stats["platform_jobs"] = total_jobs.scalar() or 0
        stats["platform_companies"] = total_companies.scalar() or 0

    return stats
