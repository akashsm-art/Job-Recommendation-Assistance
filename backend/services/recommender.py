"""
TalentSpark AI — Job Recommender Service
RAG-based intelligent job recommendations with explanations.
"""

import json
from typing import Optional


def recommend_jobs_for_user(user_data: dict, top_k: int = 10) -> list[dict]:
    """
    Generate AI-powered job recommendations for a user.
    Uses semantic similarity + multi-factor scoring + LLM explanations.
    """
    from services.embeddings import search_similar_jobs
    from services.similarity import calculate_comprehensive_match

    # Build query from user profile
    skills = []
    for key in ["technical_skills", "programming_languages", "frameworks",
                 "databases_known", "cloud_skills", "ai_skills"]:
        skills.extend(user_data.get(key) or [])

    query_parts = []
    if user_data.get("preferred_role"):
        query_parts.append(f"Job role: {user_data['preferred_role']}")
    if skills:
        query_parts.append(f"Skills: {', '.join(skills[:15])}")
    if user_data.get("experience_years"):
        query_parts.append(f"Experience: {user_data['experience_years']} years")
    if user_data.get("preferred_location"):
        query_parts.append(f"Location: {user_data['preferred_location']}")
    if user_data.get("career_objective"):
        query_parts.append(f"Career goal: {user_data['career_objective']}")

    query = "\n".join(query_parts) if query_parts else "software developer"

    # Semantic search
    filters = {}
    if user_data.get("work_mode") == "remote":
        filters["is_remote"] = True

    similar_jobs = search_similar_jobs(query, top_k=top_k * 2, filters=filters if filters else None)

    if not similar_jobs:
        return []

    # Calculate comprehensive match for each job
    recommendations = []
    for job_result in similar_jobs:
        job_data = {
            "required_skills": [s.strip() for s in job_result.get("skills", "").split(",") if s.strip()],
            "preferred_skills": [],
            "location": job_result.get("location", ""),
            "salary_min": job_result.get("salary_min", 0),
            "salary_max": job_result.get("salary_max", 0),
            "experience_min": job_result.get("experience_min", 0),
            "experience_max": job_result.get("experience_max"),
            "work_mode": job_result.get("work_mode", "onsite"),
            "is_remote": job_result.get("is_remote", False),
            "min_qualification": "",
        }

        match_result = calculate_comprehensive_match(user_data, job_data)

        # Combine semantic similarity with structured match
        semantic_score = job_result.get("score", 0) * 100
        combined_score = semantic_score * 0.4 + match_result["overall_match"] * 0.6

        # Generate reason
        matching = match_result["matching_skills"]
        missing = match_result["missing_skills"]

        reason_parts = []
        if matching:
            reason_parts.append("✔ " + " ✔ ".join(matching[:6]))
        if missing:
            reason_parts.append("Missing: ❌ " + " ❌ ".join(missing[:4]))

        reason = "\n".join(reason_parts) if reason_parts else "Good general match based on your profile"

        recommendations.append({
            "job_id": job_result["job_id"],
            "title": job_result["title"],
            "company_name": job_result.get("company_name", ""),
            "location": job_result.get("location", ""),
            "salary_range": f"{job_result.get('salary_min', 'N/A')}-{job_result.get('salary_max', 'N/A')}",
            "match_score": round(combined_score, 1),
            "match_details": match_result,
            "matching_skills": matching,
            "missing_skills": missing,
            "reason": reason,
            "semantic_score": round(semantic_score, 1),
        })

    # Sort by combined match score
    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    return recommendations[:top_k]


def generate_ai_recommendation_explanation(user_data: dict, job_data: dict, match_result: dict) -> str:
    """Use LLM to generate a detailed explanation of why a job is recommended."""
    from services.llm_service import get_llm
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a career advisor AI. Given a candidate's profile and a job listing,
explain in 2-3 sentences WHY this job is a good match for the candidate.
Be specific about skill matches, experience alignment, and growth opportunities.
Keep it encouraging and actionable."""),
        ("human", """Candidate Profile:
- Skills: {user_skills}
- Experience: {experience} years
- Preferred Role: {preferred_role}
- Location: {user_location}

Job Details:
- Title: {job_title}
- Company: {company_name}
- Required Skills: {job_skills}
- Location: {job_location}

Match Score: {match_score}%
Matching Skills: {matching_skills}
Missing Skills: {missing_skills}""")
    ])

    try:
        llm = get_llm()
        chain = prompt | llm
        response = chain.invoke({
            "user_skills": ", ".join((user_data.get("technical_skills") or [])[:10]),
            "experience": user_data.get("experience_years", 0),
            "preferred_role": user_data.get("preferred_role", "Software Developer"),
            "user_location": user_data.get("preferred_location", ""),
            "job_title": job_data.get("title", ""),
            "company_name": job_data.get("company_name", ""),
            "job_skills": ", ".join(job_data.get("required_skills") or []),
            "job_location": job_data.get("location", ""),
            "match_score": match_result.get("overall_match", 0),
            "matching_skills": ", ".join(match_result.get("matching_skills", [])),
            "missing_skills": ", ".join(match_result.get("missing_skills", [])),
        })
        return response.content
    except Exception as e:
        return f"This role aligns well with your profile (Match: {match_result.get('overall_match', 0)}%)."


def analyze_skill_gap(user_data: dict, job_data: dict) -> dict:
    """
    Analyze skill gap between user and a specific job.
    Determines if user can realistically get shortlisted.
    """
    from services.similarity import calculate_comprehensive_match

    match = calculate_comprehensive_match(user_data, job_data)
    compatibility = match["overall_match"]

    can_apply = compatibility >= 50  # 50% threshold

    if can_apply:
        message = f"Great match! You have {compatibility:.0f}% compatibility with this role."
    else:
        message = (
            f"You currently have only {compatibility:.0f}% compatibility with this role. "
            "Consider upskilling in the missing areas before applying."
        )

    return {
        "compatibility_pct": round(compatibility, 1),
        "matching_skills": match["matching_skills"],
        "missing_skills": match["missing_skills"],
        "can_apply": can_apply,
        "message": message,
        "match_details": match,
    }
