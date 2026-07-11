"""
TalentSpark AI — User/Auth Router
Authentication, profile management, and resume upload endpoints.
"""

import os
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database import get_db
from models.users import User, UserRole
from models.skill import Skill, SkillCategory, ProficiencyLevel
from models.education import Education
from models.experience import Experience
from models.project import Project
from models.certificate import Certificate
from schemas.users import (
    UserCreate, UserResponse, UserProfileResponse, CandidateProfileUpdate,
    EducationCreate, ExperienceCreate, ProjectCreate, CertificateCreate,
    ForgotPasswordRequest, ResetPasswordRequest, ChangePasswordRequest,
)
from schemas.token import Token, RefreshTokenRequest
from schemas.resume import ResumeUploadResponse
from utils.security import hash_password, verify_password
from utils.token import (
    create_access_token, create_refresh_token, verify_refresh_token,
    create_reset_token, verify_reset_token,
)
from utils.oauth2 import get_current_user, role_required

router = APIRouter(prefix="/auth", tags=["Authentication"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


# ============================================================
# Registration & Login
# ============================================================

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user (candidate or recruiter). Admin is only via admin@jobcart.com."""
    try:
        # Check if email exists
        result = await db.execute(select(User).filter(User.email == user.email))
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Email already registered")

        # Admin role logic: only admin@jobcart.com with correct password gets admin
        assigned_role = user.role
        if user.email == "admin@jobcart.com" and user.password == "jobcart007":
            assigned_role = "admin"
        elif user.role == "admin":
            raise HTTPException(status_code=403, detail="Admin registration is not allowed via signup")

        valid_roles = ["candidate", "recruiter", "admin"]
        if assigned_role not in valid_roles:
            raise HTTPException(status_code=400, detail=f"Invalid role. Must be one of: {valid_roles}")

        db_user = User(
            full_name=user.full_name,
            email=user.email,
            hashed_password=hash_password(user.password),
            role=UserRole(assigned_role),
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Login and receive access + refresh tokens."""
    try:
        result = await db.execute(select(User).filter(User.email == form_data.username))
        user = result.scalars().first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        if not user.is_active:
            raise HTTPException(status_code=403, detail="Account is deactivated")

        token_data = {"sub": str(user.id), "role": user.role.value}
        access_token = create_access_token(data=token_data)
        refresh_token = create_refresh_token(data=token_data)

        # Store refresh token
        user.refresh_token = refresh_token
        await db.commit()

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.post("/refresh", response_model=Token)
async def refresh_token(request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """Get a new access token using a refresh token."""
    payload = verify_refresh_token(request.refresh_token)
    user_id = int(payload["sub"])

    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()

    if not user or user.refresh_token != request.refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    token_data = {"sub": str(user.id), "role": user.role.value}
    new_access = create_access_token(data=token_data)
    new_refresh = create_refresh_token(data=token_data)

    user.refresh_token = new_refresh
    await db.commit()

    return Token(access_token=new_access, refresh_token=new_refresh, token_type="Bearer")


# ============================================================
# Password Reset
# ============================================================

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    """Send a password reset email."""
    result = await db.execute(select(User).filter(User.email == request.email))
    user = result.scalars().first()

    if user:
        token = create_reset_token(user.email)
        user.reset_token = token
        await db.commit()

        from services.email import send_password_reset_email
        await send_password_reset_email(user.email, token)

    # Always return success to prevent email enumeration
    return {"message": "If the email exists, a password reset link has been sent."}


@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    """Reset password using the reset token."""
    email = verify_reset_token(request.token)

    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()

    if not user or user.reset_token != request.token:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    user.hashed_password = hash_password(request.new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    await db.commit()

    return {"message": "Password has been reset successfully"}


@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Change password for authenticated user."""
    if not verify_password(request.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    current_user.hashed_password = hash_password(request.new_password)
    await db.commit()
    return {"message": "Password changed successfully"}


# ============================================================
# Profile
# ============================================================

@router.get("/me", response_model=UserProfileResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user's full profile."""
    return current_user


@router.put("/profile", response_model=UserProfileResponse)
async def update_profile(
    profile: CandidateProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update user profile (candidate profile fields)."""
    update_data = profile.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if hasattr(current_user, key):
            setattr(current_user, key, value)

    # Recalculate profile completion
    current_user.profile_completion = _calculate_profile_completion(current_user)

    await db.commit()

    # Re-fetch with relationships
    result = await db.execute(
        select(User).filter(User.id == current_user.id).options(
            selectinload(User.skills),
            selectinload(User.education_records),
            selectinload(User.experience_records),
            selectinload(User.projects),
            selectinload(User.certificates),
        )
    )
    return result.scalars().first()


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Logout and invalidate refresh token."""
    current_user.refresh_token = None
    await db.commit()
    return {"message": "Logged out successfully"}


# ============================================================
# Education, Experience, Projects, Certificates CRUD
# ============================================================

@router.post("/education")
async def add_education(
    edu: EducationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add an education record."""
    db_edu = Education(user_id=current_user.id, **edu.model_dump())
    db.add(db_edu)
    await db.commit()
    await db.refresh(db_edu)
    return db_edu


@router.post("/experience")
async def add_experience(
    exp: ExperienceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add a work experience record."""
    db_exp = Experience(user_id=current_user.id, **exp.model_dump())
    db.add(db_exp)
    await db.commit()
    await db.refresh(db_exp)
    return db_exp


@router.post("/project")
async def add_project(
    proj: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add a project."""
    db_proj = Project(user_id=current_user.id, **proj.model_dump())
    db.add(db_proj)
    await db.commit()
    await db.refresh(db_proj)
    return db_proj


@router.post("/certificate")
async def add_certificate(
    cert: CertificateCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add a certificate."""
    db_cert = Certificate(user_id=current_user.id, **cert.model_dump())
    db.add(db_cert)
    await db.commit()
    await db.refresh(db_cert)
    return db_cert


# ============================================================
# Resume Upload & Parsing
# ============================================================

@router.post("/upload-resume", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Upload and parse a resume file (PDF, DOCX, TXT)."""
    # Validate file type
    allowed_extensions = [".pdf", ".docx", ".txt"]
    ext = Path(file.filename).suffix.lower()
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}. Allowed: {allowed_extensions}"
        )

    # Save file
    filename = f"{current_user.id}_{uuid.uuid4().hex[:8]}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Parse resume
    from services.parser import parse_resume_file, extract_resume_data_with_llm
    resume_text = parse_resume_file(file_path)

    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from the uploaded file")

    # Extract structured data
    parsed_data = extract_resume_data_with_llm(resume_text)

    # Auto-populate user profile
    if parsed_data.get("full_name") and not current_user.full_name:
        current_user.full_name = parsed_data["full_name"]
    if parsed_data.get("phone") and not current_user.phone:
        current_user.phone = parsed_data["phone"]
    if parsed_data.get("technical_skills"):
        current_user.technical_skills = parsed_data["technical_skills"]
    if parsed_data.get("programming_languages"):
        current_user.programming_languages = parsed_data["programming_languages"]
    if parsed_data.get("frameworks"):
        current_user.frameworks = parsed_data["frameworks"]
    if parsed_data.get("databases"):
        current_user.databases_known = parsed_data["databases"]
    if parsed_data.get("cloud_skills"):
        current_user.cloud_skills = parsed_data["cloud_skills"]
    if parsed_data.get("ai_skills"):
        current_user.ai_skills = parsed_data["ai_skills"]
    if parsed_data.get("soft_skills"):
        current_user.soft_skills = parsed_data["soft_skills"]
    if parsed_data.get("languages"):
        current_user.languages_known = parsed_data["languages"]

    current_user.resume_url = f"/uploads/{filename}"
    current_user.resume_text = resume_text
    current_user.profile_completion = _calculate_profile_completion(current_user)

    # Run ATS analysis
    from services.ats import analyze_resume_ats
    ats_scores = analyze_resume_ats(resume_text)

    # Save ATS scores
    from models.resume_score import ResumeScore
    db_score = ResumeScore(
        user_id=current_user.id,
        **{k: v for k, v in ats_scores.items() if k in [
            "ats_score", "formatting_score", "keyword_score", "grammar_score",
            "projects_score", "experience_score", "skills_score", "education_score",
            "overall_score"
        ]},
        suggestions=ats_scores.get("suggestions"),
        missing_skills=ats_scores.get("missing_skills"),
        missing_keywords=ats_scores.get("missing_keywords"),
        strengths=ats_scores.get("strengths"),
        weaknesses=ats_scores.get("weaknesses"),
        heatmap_data=ats_scores.get("heatmap"),
    )
    db.add(db_score)

    # Embed resume into ChromaDB
    try:
        from services.embeddings import embed_user_resume
        all_skills = (parsed_data.get("skills") or []) + (parsed_data.get("technical_skills") or [])
        embed_user_resume(current_user.id, resume_text, all_skills)
    except Exception as e:
        print(f"[Resume Upload] Embedding failed: {e}")

    await db.commit()

    return ResumeUploadResponse(
        message="Resume uploaded and analyzed successfully",
        parsed_data=parsed_data,
        ats_scores=ats_scores,
        resume_url=f"/uploads/{filename}",
    )


# ============================================================
# Admin Endpoints
# ============================================================

@router.get("/users", response_model=list[UserResponse])
async def list_users(
    current_user: User = Depends(role_required(["admin"])),
    db: AsyncSession = Depends(get_db),
):
    """Admin: List all users."""
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    return result.scalars().all()


@router.put("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    current_user: User = Depends(role_required(["admin"])),
    db: AsyncSession = Depends(get_db),
):
    """Admin: Deactivate a user."""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    await db.commit()
    return {"message": f"User {user.email} deactivated"}


@router.put("/users/{user_id}/activate")
async def activate_user(
    user_id: int,
    current_user: User = Depends(role_required(["admin"])),
    db: AsyncSession = Depends(get_db),
):
    """Admin: Activate a user."""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = True
    await db.commit()
    return {"message": f"User {user.email} activated"}


# ============================================================
# Helpers
# ============================================================

def _calculate_profile_completion(user: User) -> int:
    """Calculate profile completion percentage."""
    fields = [
        user.full_name, user.phone, user.dob, user.gender, user.photo_url,
        user.linkedin, user.github, user.current_address,
        user.highest_qualification, user.university,
        user.technical_skills, user.experience_years,
        user.preferred_role, user.preferred_location,
        user.career_objective, user.resume_url,
    ]
    filled = sum(1 for f in fields if f)
    return int((filled / len(fields)) * 100)
