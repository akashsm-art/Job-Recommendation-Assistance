"""
TalentSpark AI — ATS Resume Analysis Service
Generate comprehensive ATS scores with detailed breakdown.
"""

import json
from typing import Optional


def analyze_resume_ats(resume_text: str, job_description: str = None) -> dict:
    """
    Perform comprehensive ATS analysis on a resume.
    Returns detailed scores and suggestions.
    """
    from services.llm_service import get_llm
    from langchain_core.prompts import ChatPromptTemplate

    job_context = ""
    if job_description:
        job_context = f"\n\nTarget Job Description:\n{job_description}"

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert ATS (Applicant Tracking System) Resume Analyzer.
Analyze the given resume and provide a comprehensive ATS analysis.
{job_context}

Return a valid JSON object with these exact keys and scores from 0-100:
{{
    "ats_score": 75,
    "formatting_score": 80,
    "keyword_score": 70,
    "grammar_score": 85,
    "projects_score": 65,
    "experience_score": 70,
    "skills_score": 75,
    "education_score": 80,
    "overall_score": 75,
    "suggestions": [
        "Add more quantifiable achievements",
        "Include more industry keywords",
        "..."
    ],
    "missing_skills": ["Docker", "AWS", "..."],
    "missing_keywords": ["agile", "microservices", "..."],
    "strengths": [
        "Strong technical skills section",
        "..."
    ],
    "weaknesses": [
        "Missing professional summary",
        "..."
    ],
    "heatmap": {{
        "header": 80,
        "summary": 60,
        "skills": 85,
        "experience": 70,
        "education": 75,
        "projects": 65,
        "certifications": 50,
        "links": 40
    }}
}}

Be realistic and helpful. Return ONLY valid JSON."""),
        ("human", "{resume_text}")
    ])

    try:
        llm = get_llm()
        chain = prompt | llm
        response = chain.invoke({
            "resume_text": resume_text,
            "job_context": job_context
        })
        content = response.content.strip()

        # Extract JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        return json.loads(content)

    except Exception as e:
        print(f"[ATS Service] LLM analysis failed: {e}. Using local scorer.")
        return _local_ats_analysis(resume_text)


def _local_ats_analysis(resume_text: str) -> dict:
    """Local fallback ATS analysis using heuristics."""
    text = resume_text.lower()
    text_len = len(resume_text)

    # Scoring heuristics
    formatting_score = min(100, 50 + (10 if "\n\n" in resume_text else 0) +
                          (10 if len(resume_text.split("\n")) > 10 else 0) +
                          (10 if any(c in resume_text for c in ["•", "●", "▪", "-"]) else 0) +
                          (10 if text_len > 500 else 0) +
                          (10 if text_len < 5000 else 0))

    # Keyword scoring
    important_keywords = [
        "experience", "skills", "education", "project", "certification",
        "achievement", "responsibility", "objective", "summary",
        "python", "javascript", "react", "sql", "api", "database",
        "team", "leadership", "problem solving", "communication"
    ]
    keywords_found = sum(1 for k in important_keywords if k in text)
    keyword_score = min(100, int((keywords_found / len(important_keywords)) * 100))

    # Skills detection
    tech_skills = [
        "python", "javascript", "typescript", "java", "react", "node",
        "sql", "postgresql", "mongodb", "aws", "docker", "git",
        "html", "css", "fastapi", "django", "kubernetes", "linux"
    ]
    skills_found = sum(1 for s in tech_skills if s in text)
    skills_score = min(100, int((skills_found / 8) * 100))

    # Experience scoring
    has_experience = any(w in text for w in ["experience", "work history", "employment", "worked at"])
    import re
    years_match = re.search(r'(\d+)\+?\s*(years?|yrs?)', text)
    years = int(years_match.group(1)) if years_match else 0
    experience_score = min(100, 30 + (20 if has_experience else 0) + (years * 10))

    # Education scoring
    edu_keywords = ["bachelor", "master", "b.tech", "m.tech", "bsc", "msc", "mba",
                    "phd", "degree", "university", "college", "cgpa", "gpa"]
    edu_found = sum(1 for e in edu_keywords if e in text)
    education_score = min(100, int((edu_found / 4) * 100))

    # Projects scoring
    project_indicators = ["project", "built", "developed", "created", "implemented",
                          "designed", "github.com", "deployed"]
    proj_found = sum(1 for p in project_indicators if p in text)
    projects_score = min(100, int((proj_found / 4) * 100))

    # Grammar (basic check)
    grammar_score = min(100, 60 + (10 if text[0].isupper() else 0) +
                       (10 if "." in resume_text else 0) +
                       (10 if not re.search(r'  +', resume_text) else 0) +
                       (10 if text_len > 200 else 0))

    # ATS score (weighted average)
    ats_score = int(
        keyword_score * 0.25 +
        skills_score * 0.25 +
        experience_score * 0.15 +
        education_score * 0.10 +
        projects_score * 0.10 +
        formatting_score * 0.10 +
        grammar_score * 0.05
    )

    overall_score = int(
        ats_score * 0.4 +
        skills_score * 0.2 +
        experience_score * 0.15 +
        projects_score * 0.10 +
        education_score * 0.10 +
        formatting_score * 0.05
    )

    # Generate suggestions
    suggestions = []
    missing_skills = []

    if keyword_score < 60:
        suggestions.append("Add more industry-relevant keywords to your resume")
    if skills_score < 50:
        suggestions.append("Expand your technical skills section with specific technologies")
    if experience_score < 50:
        suggestions.append("Add more detail to your work experience with quantifiable achievements")
    if education_score < 50:
        suggestions.append("Include your educational qualifications with CGPA/GPA")
    if projects_score < 50:
        suggestions.append("Add 2-3 significant projects with tech stack and outcomes")
    if formatting_score < 60:
        suggestions.append("Improve formatting with bullet points and clear section headers")
    if "linkedin" not in text:
        suggestions.append("Add your LinkedIn profile URL")
    if "github" not in text:
        suggestions.append("Include your GitHub profile for technical roles")

    # Missing skills
    for skill in ["docker", "aws", "kubernetes", "ci/cd", "microservices", "redis"]:
        if skill not in text:
            missing_skills.append(skill.title() if len(skill) > 4 else skill.upper())

    strengths = []
    if skills_score > 70:
        strengths.append("Strong technical skills section")
    if experience_score > 70:
        strengths.append("Solid work experience")
    if projects_score > 70:
        strengths.append("Good project portfolio")
    if education_score > 70:
        strengths.append("Well-documented education")
    if not strengths:
        strengths.append("Resume submitted successfully for analysis")

    weaknesses = []
    if skills_score < 50:
        weaknesses.append("Technical skills section needs improvement")
    if experience_score < 40:
        weaknesses.append("Limited work experience details")
    if projects_score < 40:
        weaknesses.append("Missing or weak projects section")
    if formatting_score < 50:
        weaknesses.append("Resume formatting needs improvement")

    return {
        "ats_score": ats_score,
        "formatting_score": formatting_score,
        "keyword_score": keyword_score,
        "grammar_score": grammar_score,
        "projects_score": projects_score,
        "experience_score": experience_score,
        "skills_score": skills_score,
        "education_score": education_score,
        "overall_score": overall_score,
        "suggestions": suggestions,
        "missing_skills": missing_skills,
        "missing_keywords": [k for k in important_keywords if k not in text][:10],
        "strengths": strengths,
        "weaknesses": weaknesses,
        "heatmap": {
            "header": min(100, formatting_score + 10),
            "summary": keyword_score,
            "skills": skills_score,
            "experience": experience_score,
            "education": education_score,
            "projects": projects_score,
            "certifications": min(100, keyword_score - 10) if keyword_score > 10 else 0,
            "links": 80 if any(w in text for w in ["linkedin", "github", "portfolio"]) else 30,
        }
    }
