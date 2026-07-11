"""
TalentSpark AI — Similarity Calculation Service
Multi-dimensional match scoring between candidates and jobs.
"""

import re
from typing import Optional


def calculate_skill_overlap(user_skills: list[str], job_skills: list[str]) -> tuple[list[str], list[str], float]:
    """
    Calculate skill overlap between user and job.
    Returns: (matching_skills, missing_skills, match_percentage)
    """
    if not job_skills:
        return [], [], 100.0

    user_set = {s.lower().strip() for s in (user_skills or [])}
    job_set = {s.lower().strip() for s in job_skills}

    matching = user_set & job_set
    missing = job_set - user_set

    match_pct = (len(matching) / len(job_set) * 100) if job_set else 100

    # Return with original casing from job_skills
    matching_display = [s for s in job_skills if s.lower().strip() in matching]
    missing_display = [s for s in job_skills if s.lower().strip() in missing]

    return matching_display, missing_display, round(match_pct, 1)


def calculate_experience_match(user_exp: float, job_min: float, job_max: float = None) -> float:
    """Calculate experience match score (0-100)."""
    if job_min is None and job_max is None:
        return 80.0  # No requirements = decent match

    user_exp = user_exp or 0

    if job_max and user_exp > job_max:
        # Overqualified — still a match but slightly lower
        return max(50, 100 - (user_exp - job_max) * 10)

    if user_exp >= (job_min or 0):
        return 100.0

    # Under-qualified
    gap = (job_min or 0) - user_exp
    return max(0, 100 - gap * 20)


def calculate_salary_match(user_expected: float, job_min: float, job_max: float) -> float:
    """Calculate salary match score (0-100)."""
    if not user_expected or (not job_min and not job_max):
        return 70.0  # Unknown = neutral match

    if job_min and job_max:
        if job_min <= user_expected <= job_max:
            return 100.0
        elif user_expected < job_min:
            return 90.0  # Candidate expects less — good for employer
        else:
            over = user_expected - job_max
            return max(20, 100 - (over / job_max * 100))
    elif job_max:
        return 100.0 if user_expected <= job_max else max(20, 100 - ((user_expected - job_max) / job_max * 50))
    elif job_min:
        return 100.0 if user_expected >= job_min else 70.0

    return 70.0


def calculate_location_match(user_location: str, job_location: str, user_work_mode: str, job_work_mode: str, job_is_remote: bool) -> float:
    """Calculate location match score (0-100)."""
    # Remote jobs match everyone
    if job_is_remote or job_work_mode == "remote":
        if user_work_mode in ["remote", None]:
            return 100.0
        return 80.0  # User prefers onsite but job is remote

    if not user_location or not job_location:
        return 60.0

    user_loc = user_location.lower().strip()
    job_loc = job_location.lower().strip()

    if user_loc == job_loc:
        return 100.0
    if user_loc in job_loc or job_loc in user_loc:
        return 90.0

    # Check city-level match
    user_cities = set(re.split(r'[,/]', user_loc))
    job_cities = set(re.split(r'[,/]', job_loc))
    if user_cities & job_cities:
        return 85.0

    # Work mode compatibility
    if user_work_mode == "hybrid" and job_work_mode == "hybrid":
        return 70.0

    return 30.0


def calculate_education_match(user_qualification: str, job_qualification: str) -> float:
    """Calculate education match score (0-100)."""
    if not job_qualification:
        return 80.0

    edu_hierarchy = {
        "phd": 6, "doctorate": 6,
        "masters": 5, "m.tech": 5, "mtech": 5, "msc": 5, "mba": 5, "m.sc": 5,
        "bachelors": 4, "b.tech": 4, "btech": 4, "bsc": 4, "b.sc": 4, "be": 4, "b.e": 4,
        "diploma": 3,
        "12th": 2, "hsc": 2, "intermediate": 2,
        "10th": 1, "ssc": 1, "matriculation": 1,
    }

    user_level = 0
    job_level = 0

    if user_qualification:
        for key, level in edu_hierarchy.items():
            if key in user_qualification.lower():
                user_level = max(user_level, level)

    for key, level in edu_hierarchy.items():
        if key in job_qualification.lower():
            job_level = max(job_level, level)

    if job_level == 0:
        return 80.0
    if user_level >= job_level:
        return 100.0
    if user_level == job_level - 1:
        return 70.0
    return max(20, 100 - (job_level - user_level) * 20)


def calculate_comprehensive_match(user_data: dict, job_data: dict) -> dict:
    """
    Calculate comprehensive multi-dimensional match scores.
    Returns dict with all match scores and explanations.
    """
    # Gather all user skills
    all_user_skills = set()
    for key in ["technical_skills", "soft_skills", "programming_languages",
                 "frameworks", "databases_known", "cloud_skills", "ai_skills"]:
        skills = user_data.get(key) or []
        all_user_skills.update(s.lower() for s in skills)

    # Also add individual Skill model entries
    for skill in user_data.get("skill_records", []):
        all_user_skills.add(skill.lower())

    all_user_skills = list(all_user_skills)

    # Job required + preferred skills
    job_required = job_data.get("required_skills") or []
    job_preferred = job_data.get("preferred_skills") or []
    all_job_skills = job_required + job_preferred

    # Calculate individual scores
    matching_skills, missing_skills, skill_pct = calculate_skill_overlap(all_user_skills, all_job_skills)

    technical_match = skill_pct
    experience_match = calculate_experience_match(
        user_data.get("experience_years", 0),
        job_data.get("experience_min"),
        job_data.get("experience_max")
    )
    location_match = calculate_location_match(
        user_data.get("preferred_location", ""),
        job_data.get("location", ""),
        user_data.get("work_mode", ""),
        job_data.get("work_mode", ""),
        job_data.get("is_remote", False)
    )
    salary_match = calculate_salary_match(
        user_data.get("expected_salary"),
        job_data.get("salary_min"),
        job_data.get("salary_max")
    )
    education_match = calculate_education_match(
        user_data.get("highest_qualification", ""),
        job_data.get("min_qualification", "")
    )

    # Soft skills match (basic)
    user_soft = [s.lower() for s in (user_data.get("soft_skills") or [])]
    soft_skills_match = min(100, len(user_soft) * 20) if user_soft else 50.0

    # Culture match (based on work mode compatibility)
    culture_match = 70.0
    if user_data.get("work_mode") == job_data.get("work_mode"):
        culture_match = 95.0
    elif job_data.get("is_remote") and user_data.get("work_mode") == "remote":
        culture_match = 100.0

    # Overall weighted score
    overall_match = (
        technical_match * 0.30 +
        experience_match * 0.20 +
        location_match * 0.15 +
        salary_match * 0.10 +
        education_match * 0.10 +
        soft_skills_match * 0.05 +
        culture_match * 0.10
    )

    return {
        "overall_match": round(overall_match, 1),
        "technical_match": round(technical_match, 1),
        "experience_match": round(experience_match, 1),
        "location_match": round(location_match, 1),
        "salary_match": round(salary_match, 1),
        "education_match": round(education_match, 1),
        "soft_skills_match": round(soft_skills_match, 1),
        "culture_match": round(culture_match, 1),
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
    }
