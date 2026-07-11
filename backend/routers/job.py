"""
TalentSpark AI — Job Router
Job CRUD, search, apply, save, and AI-powered recommendations.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_, or_, func
from typing import Optional

from database import get_db
from models.job import Job
from models.company import Company
from models.application import Application, ApplicationStatus
from models.saved_job import SavedJob
from models.users import User
from schemas.job import JobCreate, JobUpdate, JobResponse, JobSearchFilters
from schemas.application import ApplicationCreate, ApplicationResponse, ApplicationUpdate
from schemas.recommendation import JobRecommendation, SkillGapAnalysis
from utils.oauth2 import get_current_user, role_required

router = APIRouter(prefix="/job", tags=["Jobs"])


# ============================================================
# Job CRUD
# ============================================================

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=JobResponse)
async def create_job(
    job: JobCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required(["recruiter", "admin"])),
):
    """Create a new job posting (recruiter/admin only)."""
    # Verify company exists and belongs to recruiter
    result = await db.execute(select(Company).filter(Company.id == job.company_id))
    company = result.scalars().first()
    if not company:
        raise HTTPException(status_code=400, detail="Company not found")
    if current_user.role.value != "admin" and company.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only post jobs for your own company")

    db_job = Job(**job.model_dump())
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)
    return db_job


@router.get("/", response_model=list[JobResponse])
async def get_all_jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get all active jobs (public, paginated)."""
    offset = (page - 1) * page_size
    result = await db.execute(
        select(Job)
        .filter(Job.is_active == True)
        .order_by(Job.posted_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    return result.scalars().all()


@router.get("/search", response_model=list[JobResponse])
async def search_jobs(
    q: Optional[str] = None,
    location: Optional[str] = None,
    job_type: Optional[str] = None,
    work_mode: Optional[str] = None,
    salary_min: Optional[float] = None,
    salary_max: Optional[float] = None,
    experience_min: Optional[float] = None,
    experience_max: Optional[float] = None,
    is_remote: Optional[bool] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Search jobs with filters."""
    query = select(Job).filter(Job.is_active == True)

    if q:
        query = query.filter(
            or_(
                Job.title.ilike(f"%{q}%"),
                Job.description.ilike(f"%{q}%"),
            )
        )
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if job_type:
        query = query.filter(Job.job_type == job_type)
    if work_mode:
        query = query.filter(Job.work_mode == work_mode)
    if salary_min:
        query = query.filter(Job.salary_max >= salary_min)
    if salary_max:
        query = query.filter(Job.salary_min <= salary_max)
    if experience_min is not None:
        query = query.filter(Job.experience_max >= experience_min)
    if is_remote:
        query = query.filter(Job.is_remote == True)

    offset = (page - 1) * page_size
    query = query.order_by(Job.posted_at.desc()).offset(offset).limit(page_size)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, db: AsyncSession = Depends(get_db)):
    """Get job by ID (public)."""
    result = await db.execute(select(Job).filter(Job.id == job_id))
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Increment view count
    job.views_count = (job.views_count or 0) + 1
    await db.commit()

    return job


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_update: JobUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required(["recruiter", "admin"])),
):
    """Update a job posting."""
    result = await db.execute(
        select(Job).filter(Job.id == job_id).options(selectinload(Job.company))
    )
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if current_user.role.value != "admin" and job.company.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update jobs for your company")

    update_data = job_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(job, key, value)

    await db.commit()
    await db.refresh(job)
    return job


@router.delete("/{job_id}")
async def delete_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required(["recruiter", "admin"])),
):
    """Delete a job posting."""
    result = await db.execute(
        select(Job).filter(Job.id == job_id).options(selectinload(Job.company))
    )
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if current_user.role.value != "admin" and job.company.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete jobs for your company")

    await db.delete(job)
    await db.commit()
    return {"detail": "Job deleted successfully"}


# ============================================================
# Apply & Applications
# ============================================================

@router.post("/apply", response_model=ApplicationResponse)
async def apply_to_job(
    application: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required(["candidate"])),
):
    """Apply to a job with AI skill gap check."""
    # Check job exists
    result = await db.execute(
        select(Job).filter(Job.id == application.job_id).options(selectinload(Job.company))
    )
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not job.is_active:
        raise HTTPException(status_code=400, detail="This job is no longer accepting applications")

    # Check if already applied
    existing = await db.execute(
        select(Application).filter(
            Application.user_id == current_user.id,
            Application.job_id == application.job_id,
        )
    )
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="You have already applied to this job")

    # Calculate match score
    match_score = None
    match_details = None
    try:
        from services.similarity import calculate_comprehensive_match
        user_data = _user_to_dict(current_user)
        job_data = _job_to_dict(job)
        match = calculate_comprehensive_match(user_data, job_data)
        match_score = match["overall_match"]
        match_details = str(match)
    except Exception as e:
        print(f"[Apply] Match calculation error: {e}")

    db_application = Application(
        user_id=current_user.id,
        job_id=application.job_id,
        cover_letter=application.cover_letter,
        resume_snapshot=current_user.resume_text,
        match_score=match_score,
        match_details=match_details,
    )
    db.add(db_application)

    # Update application count
    job.applications_count = (job.applications_count or 0) + 1

    await db.commit()
    await db.refresh(db_application)
    return db_application


@router.get("/applications/my", response_model=list[ApplicationResponse])
async def get_my_applications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's applications."""
    result = await db.execute(
        select(Application)
        .filter(Application.user_id == current_user.id)
        .order_by(Application.applied_at.desc())
    )
    return result.scalars().all()


@router.put("/applications/{app_id}/status", response_model=ApplicationResponse)
async def update_application_status(
    app_id: int,
    update: ApplicationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required(["recruiter", "admin"])),
):
    """Update application status (recruiter/admin)."""
    result = await db.execute(select(Application).filter(Application.id == app_id))
    app = result.scalars().first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    app.status = ApplicationStatus(update.status)
    await db.commit()
    await db.refresh(app)

    # Send notification email
    try:
        from services.email import send_application_status_email
        user_result = await db.execute(select(User).filter(User.id == app.user_id))
        user = user_result.scalars().first()
        job_result = await db.execute(
            select(Job).filter(Job.id == app.job_id).options(selectinload(Job.company))
        )
        job = job_result.scalars().first()
        if user and job:
            await send_application_status_email(
                user.email, job.title, job.company.name, update.status
            )
    except Exception as e:
        print(f"[Application] Notification error: {e}")

    return app


# ============================================================
# Save / Bookmark Jobs
# ============================================================

@router.post("/{job_id}/save")
async def save_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Save/bookmark a job."""
    result = await db.execute(select(Job).filter(Job.id == job_id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Job not found")

    existing = await db.execute(
        select(SavedJob).filter(SavedJob.user_id == current_user.id, SavedJob.job_id == job_id)
    )
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="Job already saved")

    saved = SavedJob(user_id=current_user.id, job_id=job_id)
    db.add(saved)
    await db.commit()
    return {"detail": "Job saved successfully"}


@router.delete("/{job_id}/save")
async def unsave_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Remove a saved job."""
    result = await db.execute(
        select(SavedJob).filter(SavedJob.user_id == current_user.id, SavedJob.job_id == job_id)
    )
    saved = result.scalars().first()
    if not saved:
        raise HTTPException(status_code=404, detail="Saved job not found")

    await db.delete(saved)
    await db.commit()
    return {"detail": "Job unsaved successfully"}


@router.get("/saved/list", response_model=list[JobResponse])
async def get_saved_jobs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user's saved jobs."""
    result = await db.execute(
        select(Job)
        .join(SavedJob, SavedJob.job_id == Job.id)
        .filter(SavedJob.user_id == current_user.id)
        .order_by(SavedJob.saved_at.desc())
    )
    return result.scalars().all()


# ============================================================
# AI Recommendations
# ============================================================

@router.get("/recommendations/ai")
async def get_ai_recommendations(
    current_user: User = Depends(role_required(["candidate"])),
    db: AsyncSession = Depends(get_db),
):
    """Get AI-powered job recommendations for the current user."""
    from services.recommender import recommend_jobs_for_user

    user_data = _user_to_dict(current_user)
    recommendations = recommend_jobs_for_user(user_data, top_k=10)

    return {"recommendations": recommendations, "count": len(recommendations)}


@router.get("/{job_id}/skill-gap")
async def get_skill_gap(
    job_id: int,
    current_user: User = Depends(role_required(["candidate"])),
    db: AsyncSession = Depends(get_db),
):
    """Analyze skill gap between candidate and a specific job."""
    result = await db.execute(
        select(Job).filter(Job.id == job_id).options(selectinload(Job.company))
    )
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    from services.recommender import analyze_skill_gap

    user_data = _user_to_dict(current_user)
    job_data = _job_to_dict(job)
    analysis = analyze_skill_gap(user_data, job_data)

    # Add course recommendations for missing skills
    if analysis["missing_skills"]:
        from services.course_recommender import recommend_courses_for_skills
        analysis["recommended_courses"] = recommend_courses_for_skills(analysis["missing_skills"])

    return analysis


# ============================================================
# Recruiter: Applicant Management
# ============================================================

@router.get("/{job_id}/applicants", response_model=list[ApplicationResponse])
async def get_job_applicants(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required(["recruiter", "admin"])),
):
    """Get all applicants for a job (recruiter/admin only)."""
    result = await db.execute(
        select(Job).filter(Job.id == job_id).options(selectinload(Job.company))
    )
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if current_user.role.value != "admin" and job.company.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    result = await db.execute(
        select(Application)
        .filter(Application.job_id == job_id)
        .order_by(Application.match_score.desc().nullslast())
    )
    return result.scalars().all()


# ============================================================
# Helpers
# ============================================================

def _user_to_dict(user: User) -> dict:
    """Convert User model to dict for service functions."""
    skill_records = [s.name for s in (user.skills or [])]
    return {
        "technical_skills": user.technical_skills or [],
        "soft_skills": user.soft_skills or [],
        "programming_languages": user.programming_languages or [],
        "frameworks": user.frameworks or [],
        "databases_known": user.databases_known or [],
        "cloud_skills": user.cloud_skills or [],
        "ai_skills": user.ai_skills or [],
        "skill_records": skill_records,
        "experience_years": user.experience_years or 0,
        "preferred_role": user.preferred_role,
        "preferred_location": user.preferred_location,
        "expected_salary": user.expected_salary,
        "work_mode": user.work_mode.value if user.work_mode else None,
        "highest_qualification": user.highest_qualification,
        "career_objective": user.career_objective,
    }


def _job_to_dict(job: Job) -> dict:
    """Convert Job model to dict for service functions."""
    return {
        "title": job.title,
        "required_skills": job.required_skills or [],
        "preferred_skills": job.preferred_skills or [],
        "location": job.location,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
        "experience_min": job.experience_min,
        "experience_max": job.experience_max,
        "work_mode": job.work_mode.value if job.work_mode else "onsite",
        "is_remote": job.is_remote,
        "min_qualification": job.min_qualification,
        "company_name": job.company.name if job.company else "",
    }
