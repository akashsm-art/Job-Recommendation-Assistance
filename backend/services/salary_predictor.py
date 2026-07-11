"""
TalentSpark AI — AI Salary Predictor Service
Predicts expected salary based on skills, experience, location, role, and market data.
"""

import json


# --- Market salary data (Indian IT market, LPA = Lakhs Per Annum) ---
SALARY_BENCHMARKS = {
    # Role -> {experience_range: (min_lpa, max_lpa)}
    "software engineer": {(0, 1): (3, 6), (1, 3): (6, 12), (3, 5): (10, 20), (5, 8): (18, 35), (8, 99): (30, 60)},
    "frontend developer": {(0, 1): (3, 5), (1, 3): (5, 10), (3, 5): (10, 18), (5, 8): (15, 30), (8, 99): (25, 50)},
    "backend developer": {(0, 1): (3, 6), (1, 3): (6, 12), (3, 5): (12, 22), (5, 8): (20, 38), (8, 99): (32, 60)},
    "full stack developer": {(0, 1): (3, 6), (1, 3): (6, 14), (3, 5): (12, 24), (5, 8): (22, 40), (8, 99): (35, 65)},
    "data scientist": {(0, 1): (4, 8), (1, 3): (8, 16), (3, 5): (15, 28), (5, 8): (25, 45), (8, 99): (40, 75)},
    "data analyst": {(0, 1): (3, 5), (1, 3): (5, 10), (3, 5): (8, 16), (5, 8): (14, 25), (8, 99): (20, 40)},
    "devops engineer": {(0, 1): (4, 7), (1, 3): (7, 14), (3, 5): (12, 24), (5, 8): (22, 40), (8, 99): (35, 60)},
    "ml engineer": {(0, 1): (5, 9), (1, 3): (9, 18), (3, 5): (16, 30), (5, 8): (28, 50), (8, 99): (45, 80)},
    "ai engineer": {(0, 1): (5, 10), (1, 3): (10, 20), (3, 5): (18, 35), (5, 8): (30, 55), (8, 99): (50, 90)},
    "product manager": {(0, 1): (6, 10), (1, 3): (10, 18), (3, 5): (16, 30), (5, 8): (28, 50), (8, 99): (40, 75)},
    "qa engineer": {(0, 1): (3, 5), (1, 3): (5, 9), (3, 5): (8, 15), (5, 8): (13, 25), (8, 99): (20, 40)},
    "mobile developer": {(0, 1): (3, 6), (1, 3): (6, 12), (3, 5): (10, 22), (5, 8): (20, 38), (8, 99): (30, 55)},
    "cloud architect": {(0, 1): (5, 8), (1, 3): (8, 16), (3, 5): (15, 30), (5, 8): (28, 50), (8, 99): (45, 80)},
    "cybersecurity analyst": {(0, 1): (4, 7), (1, 3): (7, 14), (3, 5): (12, 24), (5, 8): (22, 40), (8, 99): (35, 60)},
}

# Premium skill multipliers
SKILL_PREMIUMS = {
    "kubernetes": 1.12, "aws": 1.10, "gcp": 1.10, "azure": 1.08,
    "docker": 1.06, "terraform": 1.10, "machine learning": 1.15,
    "deep learning": 1.18, "nlp": 1.15, "computer vision": 1.15,
    "pytorch": 1.12, "tensorflow": 1.10, "langchain": 1.15,
    "rust": 1.12, "golang": 1.10, "scala": 1.08,
    "system design": 1.10, "microservices": 1.08,
    "kafka": 1.10, "redis": 1.06, "elasticsearch": 1.08,
    "graphql": 1.06, "react": 1.05, "next.js": 1.06,
    "typescript": 1.05, "fastapi": 1.06,
}

# City multipliers
CITY_MULTIPLIERS = {
    "bangalore": 1.15, "bengaluru": 1.15, "hyderabad": 1.10,
    "pune": 1.05, "mumbai": 1.12, "delhi": 1.08, "ncr": 1.08,
    "gurgaon": 1.10, "noida": 1.06, "chennai": 1.05,
    "kolkata": 0.95, "ahmedabad": 0.95, "jaipur": 0.90,
    "remote": 1.08, "usa": 3.5, "uk": 2.5, "europe": 2.2,
    "singapore": 2.8, "dubai": 2.0, "canada": 2.8, "australia": 2.5,
}


def predict_salary(
    role: str,
    experience_years: float,
    skills: list[str],
    location: str = None,
    current_ctc: float = None,
    education: str = None,
) -> dict:
    """
    Predict expected salary based on role, experience, skills, and location.
    Returns salary range with confidence and factors.
    """
    role_lower = role.lower().strip()
    exp = experience_years or 0

    # Find base salary range
    base_min, base_max = _get_base_salary(role_lower, exp)

    # Apply skill premiums
    skill_multiplier = 1.0
    premium_skills_applied = []
    for skill in (skills or []):
        skill_lower = skill.lower().strip()
        if skill_lower in SKILL_PREMIUMS:
            skill_multiplier *= SKILL_PREMIUMS[skill_lower]
            premium_skills_applied.append(skill)
    # Cap skill multiplier
    skill_multiplier = min(skill_multiplier, 1.8)

    # Apply location multiplier
    loc_multiplier = 1.0
    if location:
        loc_lower = location.lower().strip()
        for city, mult in CITY_MULTIPLIERS.items():
            if city in loc_lower:
                loc_multiplier = mult
                break

    # Apply education boost
    edu_multiplier = 1.0
    if education:
        edu_lower = education.lower()
        if any(w in edu_lower for w in ["phd", "doctorate"]):
            edu_multiplier = 1.15
        elif any(w in edu_lower for w in ["masters", "m.tech", "mtech", "mba"]):
            edu_multiplier = 1.08
        elif any(w in edu_lower for w in ["iit", "nit", "bits", "iiit"]):
            edu_multiplier = 1.12

    # Calculate final range
    adjusted_min = base_min * skill_multiplier * loc_multiplier * edu_multiplier
    adjusted_max = base_max * skill_multiplier * loc_multiplier * edu_multiplier

    # Calculate confidence based on data quality
    confidence = 75
    if role_lower in SALARY_BENCHMARKS:
        confidence += 10
    if premium_skills_applied:
        confidence += 5
    if location:
        confidence += 5
    confidence = min(confidence, 95)

    # Compute recommended CTC
    recommended = (adjusted_min + adjusted_max) / 2

    # Compute hike percentage if current CTC provided
    hike_pct = None
    if current_ctc and current_ctc > 0:
        hike_pct = round(((recommended - current_ctc) / current_ctc) * 100, 1)

    # Factors breakdown
    factors = []
    if role_lower in SALARY_BENCHMARKS:
        factors.append(f"📊 Role '{role}' has strong market data")
    factors.append(f"⏳ {exp} years experience → base range ₹{base_min:.1f}-{base_max:.1f} LPA")
    if premium_skills_applied:
        factors.append(f"🚀 Premium skills boost ({', '.join(premium_skills_applied[:5])}) → {skill_multiplier:.2f}x")
    if loc_multiplier != 1.0:
        factors.append(f"📍 Location '{location}' → {loc_multiplier:.2f}x multiplier")
    if edu_multiplier != 1.0:
        factors.append(f"🎓 Education boost → {edu_multiplier:.2f}x")

    return {
        "predicted_min_lpa": round(adjusted_min, 1),
        "predicted_max_lpa": round(adjusted_max, 1),
        "recommended_ctc_lpa": round(recommended, 1),
        "confidence_pct": confidence,
        "currency": "INR",
        "hike_percentage": hike_pct,
        "factors": factors,
        "premium_skills": premium_skills_applied,
        "market_trend": "📈 Upward" if skill_multiplier > 1.1 else "➡️ Stable",
        "comparable_roles": _get_comparable_roles(role_lower),
    }


def predict_salary_with_llm(user_data: dict) -> dict:
    """Use LLM for a more nuanced salary prediction."""
    from services.llm_service import get_llm
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a compensation analyst specializing in the Indian and global tech job market.
Given a candidate's profile, predict their expected salary range.
Return a valid JSON object:
{{
    "predicted_min_lpa": 10,
    "predicted_max_lpa": 18,
    "recommended_ctc_lpa": 14,
    "confidence_pct": 80,
    "reasoning": "Detailed explanation",
    "negotiation_tips": ["Tip 1", "Tip 2"],
    "market_insight": "Brief market insight for this role"
}}
Return ONLY valid JSON."""),
        ("human", """Profile:
Role: {role}
Experience: {experience} years
Skills: {skills}
Location: {location}
Current CTC: {current_ctc} LPA
Education: {education}
Company: {company}""")
    ])

    try:
        llm = get_llm()
        chain = prompt | llm
        response = chain.invoke({
            "role": user_data.get("preferred_role", "Software Engineer"),
            "experience": user_data.get("experience_years", 0),
            "skills": ", ".join((user_data.get("technical_skills") or [])[:15]),
            "location": user_data.get("preferred_location", "India"),
            "current_ctc": user_data.get("current_ctc", "Not disclosed"),
            "education": user_data.get("highest_qualification", "B.Tech"),
            "company": user_data.get("current_company", "Not disclosed"),
        })
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        print(f"[Salary Predictor] LLM failed: {e}")
        return predict_salary(
            role=user_data.get("preferred_role", "Software Engineer"),
            experience_years=user_data.get("experience_years", 0),
            skills=user_data.get("technical_skills", []),
            location=user_data.get("preferred_location"),
            current_ctc=user_data.get("current_ctc"),
            education=user_data.get("highest_qualification"),
        )


def _get_base_salary(role: str, experience: float) -> tuple[float, float]:
    """Get base salary range from benchmarks."""
    benchmarks = SALARY_BENCHMARKS.get(role)
    if not benchmarks:
        # Fallback: try partial match
        for key, data in SALARY_BENCHMARKS.items():
            if key in role or role in key:
                benchmarks = data
                break

    if not benchmarks:
        benchmarks = SALARY_BENCHMARKS["software engineer"]

    for (low, high), (sal_min, sal_max) in benchmarks.items():
        if low <= experience < high:
            return sal_min, sal_max

    return 5, 15  # Default fallback


def _get_comparable_roles(role: str) -> list[str]:
    """Get comparable roles for salary comparison."""
    role_families = {
        "software engineer": ["Full Stack Developer", "Backend Developer", "Frontend Developer"],
        "data scientist": ["ML Engineer", "AI Engineer", "Data Analyst"],
        "devops engineer": ["Cloud Architect", "SRE", "Platform Engineer"],
        "product manager": ["Technical Program Manager", "Business Analyst"],
        "frontend developer": ["React Developer", "UI Engineer", "Full Stack Developer"],
        "backend developer": ["Software Engineer", "API Developer", "Full Stack Developer"],
    }
    return role_families.get(role, ["Software Engineer", "Full Stack Developer"])
