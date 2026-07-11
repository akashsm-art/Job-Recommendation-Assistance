"""
TalentSpark AI — User Schemas
Pydantic models for user registration, login, profile, and responses.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime


# --- Registration ---
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str = "candidate"  # "candidate", "recruiter", "admin"


# --- Login ---
class LoginUser(BaseModel):
    email: EmailStr
    password: str


# --- Profile Update (Candidate) ---
class CandidateProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    photo_url: Optional[str] = None
    nationality: Optional[str] = None
    languages_known: Optional[list[str]] = None

    # Address
    current_address: Optional[str] = None
    permanent_address: Optional[str] = None

    # Social
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    leetcode: Optional[str] = None
    hackerrank: Optional[str] = None
    codechef: Optional[str] = None
    codeforces: Optional[str] = None

    # Professional
    current_company: Optional[str] = None
    current_ctc: Optional[float] = None
    expected_ctc: Optional[float] = None
    experience_years: Optional[float] = None
    notice_period: Optional[str] = None
    availability: Optional[str] = None

    # Preferences
    preferred_role: Optional[str] = None
    preferred_location: Optional[str] = None
    expected_salary: Optional[float] = None
    work_mode: Optional[str] = None

    # Education
    highest_qualification: Optional[str] = None
    university: Optional[str] = None
    cgpa: Optional[float] = None

    # Career
    career_objective: Optional[str] = None

    # Skills (JSON arrays)
    technical_skills: Optional[list[str]] = None
    soft_skills: Optional[list[str]] = None
    programming_languages: Optional[list[str]] = None
    frameworks: Optional[list[str]] = None
    databases_known: Optional[list[str]] = None
    cloud_skills: Optional[list[str]] = None
    ai_skills: Optional[list[str]] = None


# --- Skill Schema ---
class SkillSchema(BaseModel):
    id: int
    name: str
    category: str
    proficiency: str

    class Config:
        from_attributes = True


# --- Education Schema ---
class EducationSchema(BaseModel):
    id: int
    degree: str
    field_of_study: Optional[str] = None
    institution: str
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    cgpa: Optional[float] = None

    class Config:
        from_attributes = True


class EducationCreate(BaseModel):
    degree: str
    field_of_study: Optional[str] = None
    institution: str
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    cgpa: Optional[float] = None


# --- Experience Schema ---
class ExperienceSchema(BaseModel):
    id: int
    company: str
    role: str
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: bool = False
    description: Optional[str] = None

    class Config:
        from_attributes = True


class ExperienceCreate(BaseModel):
    company: str
    role: str
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: bool = False
    description: Optional[str] = None


# --- Project Schema ---
class ProjectSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    tech_stack: Optional[list[str]] = None
    url: Optional[str] = None
    github_url: Optional[str] = None

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    tech_stack: Optional[list[str]] = None
    url: Optional[str] = None
    github_url: Optional[str] = None


# --- Certificate Schema ---
class CertificateSchema(BaseModel):
    id: int
    name: str
    issuer: Optional[str] = None
    credential_url: Optional[str] = None

    class Config:
        from_attributes = True


class CertificateCreate(BaseModel):
    name: str
    issuer: Optional[str] = None
    issue_date: Optional[date] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None


# --- User Response ---
class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    photo_url: Optional[str] = None
    is_verified: bool = False
    is_active: bool = True
    profile_completion: int = 0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Full Profile Response ---
class UserProfileResponse(BaseModel):
    id: int
    email: str
    role: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    photo_url: Optional[str] = None
    nationality: Optional[str] = None
    languages_known: Optional[list[str]] = None
    current_address: Optional[str] = None
    permanent_address: Optional[str] = None

    # Social
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    leetcode: Optional[str] = None
    hackerrank: Optional[str] = None
    codechef: Optional[str] = None
    codeforces: Optional[str] = None

    # Professional
    current_company: Optional[str] = None
    current_ctc: Optional[float] = None
    expected_ctc: Optional[float] = None
    experience_years: Optional[float] = None
    notice_period: Optional[str] = None
    availability: Optional[str] = None
    preferred_role: Optional[str] = None
    preferred_location: Optional[str] = None
    expected_salary: Optional[float] = None
    work_mode: Optional[str] = None

    # Education
    highest_qualification: Optional[str] = None
    university: Optional[str] = None
    cgpa: Optional[float] = None
    career_objective: Optional[str] = None
    resume_url: Optional[str] = None

    # Skills
    technical_skills: Optional[list[str]] = None
    soft_skills: Optional[list[str]] = None
    programming_languages: Optional[list[str]] = None
    frameworks: Optional[list[str]] = None
    databases_known: Optional[list[str]] = None
    cloud_skills: Optional[list[str]] = None
    ai_skills: Optional[list[str]] = None

    # Profile
    profile_completion: int = 0
    is_verified: bool = False
    is_active: bool = True

    # Nested
    skills: list[SkillSchema] = []
    education_records: list[EducationSchema] = []
    experience_records: list[ExperienceSchema] = []
    projects: list[ProjectSchema] = []
    certificates: list[CertificateSchema] = []

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Password Reset ---
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
