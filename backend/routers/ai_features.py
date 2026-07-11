"""
TalentSpark AI — Phase 2 Advanced AI Features Router
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database import get_db
from models.users import User
from models.job import Job
from models.company import Company
from models.application import Application
from utils.oauth2 import get_current_user, role_required

from schemas.ai_features import (
    SalaryPredictionRequest, SalaryPredictionResponse,
    CareerRoadmapRequest, CareerRoadmapResponse,
    ResumeRewriteRequest, ResumeRewriteResponse,
    CoverLetterRequest, CoverLetterResponse,
    InterviewPrepRequest, InterviewPrepResponse,
    MockInterviewResponse,
    InterviewAnswerEvaluationRequest, InterviewAnswerEvaluationResponse,
    CompanyFitRequest, CompanyFitResponse,
    SkillTrendRequest, SkillTrendResponse,
    JobMarketOverviewResponse, UserSkillValueAnalysisResponse,
    ResumeBuildRequest, ResumeBuildResponse, ResumeHtmlResponse,
    RankCandidatesRequest, CandidateRankingResponse,
    DuplicateDetectionRequest, DuplicateDetectionResponse,
    ResumeAuthenticityRequest, ResumeAuthenticityResponse,
    RecruiterPoolSummaryResponse,
)

router = APIRouter(prefix="/ai", tags=["AI Advanced Features"])


# ============================================================
# Candidate / Core AI Features
# ============================================================

@router.post("/predict-salary", response_model=SalaryPredictionResponse)
async def predict_candidate_salary(
    request: SalaryPredictionRequest,
    current_user: User = Depends(get_current_user),
):
    """Predict candidate expected salary based on credentials & role."""
    from services.salary_predictor import predict_salary, predict_salary_with_llm

    if request.use_llm:
        user_data = {
            "preferred_role": request.role,
            "experience_years": request.experience_years,
            "technical_skills": request.skills,
            "preferred_location": request.location,
            "current_ctc": request.current_ctc,
            "highest_qualification": request.education,
            "current_company": None,
        }
        res = predict_salary_with_llm(user_data)
        # Handle schema differences if LLM is used
        return SalaryPredictionResponse(
            predicted_min_lpa=res.get("predicted_min_lpa", 0.0),
            predicted_max_lpa=res.get("predicted_max_lpa", 0.0),
            recommended_ctc_lpa=res.get("recommended_ctc_lpa", 0.0),
            confidence_pct=res.get("confidence_pct", 75),
            currency="INR",
            factors=res.get("factors") or [],
            premium_skills=res.get("premium_skills") or [],
            market_trend=res.get("market_trend", "➡️ Stable"),
            comparable_roles=res.get("comparable_roles") or [],
            reasoning=res.get("reasoning"),
            negotiation_tips=res.get("negotiation_tips"),
            market_insight=res.get("market_insight"),
        )

    res = predict_salary(
        role=request.role,
        experience_years=request.experience_years,
        skills=request.skills,
        location=request.location,
        current_ctc=request.current_ctc,
        education=request.education,
    )
    return res


@router.post("/career-roadmap", response_model=CareerRoadmapResponse)
async def get_candidate_career_roadmap(
    request: CareerRoadmapRequest,
    current_user: User = Depends(get_current_user),
):
    """Generate custom or templated career path roadmap."""
    from services.career_roadmap import generate_career_roadmap

    # Collect current user skills
    skills = []
    for key in ["technical_skills", "programming_languages", "frameworks", "databases_known", "cloud_skills"]:
        skills.extend(getattr(current_user, key) or [])
    skills.extend([s.name for s in (current_user.skills or [])])

    res = generate_career_roadmap(
        current_skills=skills,
        target_role=request.target_role,
        experience_years=current_user.experience_years or 0,
    )
    return res


@router.post("/rewrite-resume", response_model=ResumeRewriteResponse)
async def rewrite_resume_endpoint(
    request: ResumeRewriteRequest,
    current_user: User = Depends(get_current_user),
):
    """AI-powered resume optimization for a specific role and JD context."""
    from services.resume_writer import rewrite_resume
    res = rewrite_resume(
        resume_text=request.resume_text,
        target_role=request.target_role,
        job_description=request.job_description,
    )
    return res


@router.post("/generate-cover-letter", response_model=CoverLetterResponse)
async def generate_cover_letter_endpoint(
    request: CoverLetterRequest,
    current_user: User = Depends(get_current_user),
):
    """Generate cover letter tailored to a role, company, and JD."""
    from services.resume_writer import generate_cover_letter

    skills = []
    for key in ["technical_skills", "programming_languages", "frameworks"]:
        skills.extend(getattr(current_user, key) or [])
    skills.extend([s.name for s in (current_user.skills or [])])

    res = generate_cover_letter(
        user_name=current_user.full_name or "Candidate",
        target_role=request.target_role,
        company_name=request.company_name,
        user_skills=skills,
        experience_years=current_user.experience_years or 0,
        resume_text=current_user.resume_text,
        job_description=request.job_description,
        tone=request.tone,
    )
    return res


@router.post("/interview-prep", response_model=InterviewPrepResponse)
async def get_interview_prep(
    request: InterviewPrepRequest,
    current_user: User = Depends(get_current_user),
):
    """Get interview prep material including MCQs, coding challenges, design topics."""
    from services.interview_service import generate_interview_prep

    skills = []
    for key in ["technical_skills", "programming_languages"]:
        skills.extend(getattr(current_user, key) or [])

    res = generate_interview_prep(
        role=request.role,
        difficulty=request.difficulty,
        categories=request.categories,
        num_questions=request.num_questions,
        company=request.company,
        user_skills=skills,
    )
    return res


@router.get("/mock-interview", response_model=MockInterviewResponse)
async def get_mock_interview_endpoint(
    role: str,
    difficulty: str = "Medium",
    rounds: int = 3,
    current_user: User = Depends(get_current_user),
):
    """Get structured mock interview rounds."""
    from services.interview_service import generate_mock_interview
    res = generate_mock_interview(role, difficulty, rounds)
    return res


@router.post("/evaluate-answer", response_model=InterviewAnswerEvaluationResponse)
async def evaluate_interview_answer(
    request: InterviewAnswerEvaluationRequest,
    current_user: User = Depends(get_current_user),
):
    """AI evaluation of candidate interview answers."""
    from services.interview_service import evaluate_interview_response
    res = evaluate_interview_response(request.question, request.answer, request.role)
    return res


@router.post("/company-fit", response_model=CompanyFitResponse)
async def predict_candidate_company_fit(
    request: CompanyFitRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Evaluate candidate culture, technology, and industry fit for a company."""
    result = await db.execute(select(Company).filter(Company.id == request.company_id))
    company = result.scalars().first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    from services.company_fit import predict_company_fit, predict_company_fit_with_llm

    user_data = _user_to_dict(current_user)
    company_data = {
        "name": company.name,
        "industry": company.industry,
        "company_size": company.company_size,
        "tech_stack": company.tech_stack,
        "headquarters": company.headquarters,
        "locations": company.locations,
        "culture": company.culture,
    }

    if request.use_llm:
        res = predict_company_fit_with_llm(user_data, company_data)
        # Support schema mapping
        return CompanyFitResponse(
            scores=res.get("dimensions", {}),
            recommendation=res.get("recommendation", ""),
            matching_tech=[],
            missing_tech=[],
            insights=res.get("pros", []) + res.get("cons", []),
            overall_fit_pct=res.get("overall_fit_pct"),
            dimensions=res.get("dimensions"),
            pros=res.get("pros"),
            cons=res.get("cons"),
            questions_to_ask=res.get("questions_to_ask"),
        )

    res = predict_company_fit(user_data, company_data)
    return res


# ============================================================
# Market & Skill Trends
# ============================================================

@router.post("/skill-trends", response_model=SkillTrendResponse)
async def get_skill_trends_endpoint(
    request: SkillTrendRequest,
    current_user: User = Depends(get_current_user),
):
    """Get market trend details for skills (grouped or specific)."""
    from services.skill_trends import get_skill_trends
    res = get_skill_trends(request.skills)
    return res


@router.get("/market-overview", response_model=JobMarketOverviewResponse)
async def get_job_market_overview_endpoint(
    current_user: User = Depends(get_current_user),
):
    """Get overall market dashboard updates, hot roles, growing tech."""
    from services.skill_trends import get_job_market_overview
    res = get_job_market_overview()
    return res


@router.get("/skill-value-analysis", response_model=UserSkillValueAnalysisResponse)
async def analyze_user_skills(
    current_user: User = Depends(get_current_user),
):
    """Analyze current candidate profile skills for market value & hikes."""
    from services.skill_trends import analyze_user_skill_market_value

    skills = []
    for key in ["technical_skills", "programming_languages", "frameworks", "databases_known", "cloud_skills"]:
        skills.extend(getattr(current_user, key) or [])
    skills.extend([s.name for s in (current_user.skills or [])])

    if not skills:
        return {
            "trending_skills": [],
            "stable_skills": [],
            "declining_skills": [],
            "untracked_skills": [],
            "estimated_salary_boost_pct": 0.0,
            "market_readiness": {"score": 0, "level": "🔴 Needs Improvement", "trending_pct": 0, "declining_pct": 0},
            "recommendations": ["Add skills to your profile to get personalized market analysis."],
        }

    res = analyze_user_skill_market_value(skills)
    return res


# ============================================================
# Resume Builder
# ============================================================

@router.post("/build-resume", response_model=ResumeBuildResponse)
async def build_candidate_resume(
    request: ResumeBuildRequest,
    current_user: User = Depends(get_current_user),
):
    """Generate structured resume data using templates (modern, minimal, corporate, etc.)."""
    from services.resume_builder import generate_resume_content
    user_data = _user_to_dict(current_user)
    res = generate_resume_content(user_data, request.target_role, request.template)
    return res


@router.post("/build-resume/html", response_model=ResumeHtmlResponse)
async def build_candidate_resume_html(
    request: ResumeBuildRequest,
    current_user: User = Depends(get_current_user),
):
    """Generate HTML format resume for immediate browser view or PDF print."""
    from services.resume_builder import generate_resume_html
    user_data = _user_to_dict(current_user)
    html = generate_resume_html(user_data, request.template, request.target_role)
    return ResumeHtmlResponse(html=html)


# ============================================================
# Recruiter AI Tools (Role Restricted)
# ============================================================

@router.post("/rank-candidates", response_model=CandidateRankingResponse)
async def rank_candidates_endpoint(
    request: RankCandidatesRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required(["recruiter", "admin"])),
):
    """Recruiter: Rank applicants for a specific job description."""
    # Find job
    job_result = await db.execute(select(Job).filter(Job.id == request.job_id).options(selectinload(Job.company)))
    job = job_result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if current_user.role.value != "admin" and job.company.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied. You do not own this company.")

    # Find applicants
    app_result = await db.execute(
        select(Application)
        .filter(Application.job_id == request.job_id)
    )
    apps = app_result.scalars().all()
    if not apps:
        return CandidateRankingResponse(ranked_candidates=[])

    user_ids = [a.user_id for a in apps]
    user_result = await db.execute(
        select(User)
        .filter(User.id.in_(user_ids))
        .options(
            selectinload(User.skills),
            selectinload(User.education_records),
            selectinload(User.experience_records),
            selectinload(User.projects),
            selectinload(User.certificates),
        )
    )
    users = user_result.scalars().all()

    candidates_data = [_user_to_dict(u) for u in users]
    job_data = {
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
    }

    from services.recruiter_ai import rank_candidates_for_job
    ranked = rank_candidates_for_job(job_data, candidates_data)
    return CandidateRankingResponse(ranked_candidates=ranked)


@router.post("/detect-duplicates", response_model=DuplicateDetectionResponse)
async def check_duplicates(
    request: DuplicateDetectionRequest,
    current_user: User = Depends(role_required(["recruiter", "admin"])),
):
    """Recruiter: Check two resumes for high similarity or duplicate submission."""
    from services.recruiter_ai import detect_duplicate_resumes
    res = detect_duplicate_resumes(request.resume_text_1, request.resume_text_2)
    return res


@router.post("/resume-authenticity", response_model=ResumeAuthenticityResponse)
async def verify_resume_authenticity(
    request: ResumeAuthenticityRequest,
    current_user: User = Depends(role_required(["recruiter", "admin"])),
):
    """Recruiter: Scan candidate resume text for fake claims, stuffed skills, or inconsistencies."""
    from services.recruiter_ai import analyze_resume_authenticity
    res = analyze_resume_authenticity(request.resume_text)
    return res


@router.get("/pool-summary/{job_id}", response_model=RecruiterPoolSummaryResponse)
async def get_pool_summary(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required(["recruiter", "admin"])),
):
    """Recruiter: Get overall applicant analytics and pool suitability report."""
    job_result = await db.execute(select(Job).filter(Job.id == job_id).options(selectinload(Job.company)))
    job = job_result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if current_user.role.value != "admin" and job.company.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    app_result = await db.execute(select(Application).filter(Application.job_id == job_id))
    apps = app_result.scalars().all()

    applicants_list = []
    for app in apps:
        # Load user skills
        user_res = await db.execute(
            select(User).filter(User.id == app.user_id).options(selectinload(User.skills))
        )
        user = user_res.scalars().first()
        if user:
            # Reconstruct list of matching skills
            match_details = app.match_details or "{}"
            import ast
            try:
                details = ast.literal_eval(match_details)
            except:
                details = {}
            applicants_list.append({
                "match_score": app.match_score,
                "matching_skills": details.get("matching_skills", []),
            })

    job_data = {"title": job.title}

    from services.recruiter_ai import generate_recruiter_summary
    res = generate_recruiter_summary(job_data, applicants_list)
    return res


# ============================================================
# Helpers
# ============================================================

def _user_to_dict(user: User) -> dict:
    """Helper to convert User model with loaded relations to dict for services."""
    skill_records = [s.name for s in (user.skills or [])]

    # Convert records lists to dicts
    edu_list = []
    for record in (user.education_records or []):
        edu_list.append({
            "id": record.id,
            "degree": record.degree,
            "institution": record.institution,
            "cgpa": record.cgpa,
            "end_year": record.end_year,
        })

    exp_list = []
    for record in (user.experience_records or []):
        exp_list.append({
            "id": record.id,
            "company": record.company,
            "role": record.role,
            "start_date": str(record.start_date) if record.start_date else "",
            "end_date": str(record.end_date) if record.end_date else "",
            "description": record.description,
        })

    proj_list = []
    for record in (user.projects or []):
        proj_list.append({
            "id": record.id,
            "title": record.title,
            "description": record.description,
            "tech_stack": record.tech_stack,
        })

    cert_list = []
    for record in (user.certificates or []):
        cert_list.append({
            "id": record.id,
            "name": record.name,
            "issuer": record.issuer,
        })

    return {
        "id": user.id,
        "full_name": user.full_name or "Candidate",
        "email": user.email,
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
        "education_records": edu_list,
        "experience_records": exp_list,
        "projects": proj_list,
        "certificates": cert_list,
    }
