"""
TalentSpark AI — AI Company Fit Prediction
Predicts how well a candidate fits a specific company's culture and requirements.
"""

import json


def predict_company_fit(user_data: dict, company_data: dict) -> dict:
    """
    Predict company-candidate fit across multiple dimensions.
    """
    scores = {}

    # 1. Technical Fit
    user_skills = set()
    for key in ["technical_skills", "programming_languages", "frameworks", "databases_known", "cloud_skills"]:
        user_skills.update(s.lower() for s in (user_data.get(key) or []))

    company_tech = set(s.lower() for s in (company_data.get("tech_stack") or []))
    if company_tech:
        tech_overlap = len(user_skills & company_tech)
        scores["technical_fit"] = min(100, round((tech_overlap / max(len(company_tech), 1)) * 100))
    else:
        scores["technical_fit"] = 60  # Neutral if no data

    # 2. Culture Fit (work mode, benefits preferences)
    culture_score = 60
    if user_data.get("work_mode") and company_data.get("culture"):
        culture_lower = (company_data.get("culture") or "").lower()
        if user_data["work_mode"] == "remote" and "remote" in culture_lower:
            culture_score = 95
        elif "flexible" in culture_lower:
            culture_score = 85
    scores["culture_fit"] = culture_score

    # 3. Industry Fit
    industry_score = 70
    if user_data.get("career_objective"):
        obj_lower = user_data["career_objective"].lower()
        industry = (company_data.get("industry") or "").lower()
        if industry and industry in obj_lower:
            industry_score = 90
    scores["industry_fit"] = industry_score

    # 4. Size Fit
    size_score = 70
    company_size = company_data.get("company_size", "")
    exp = user_data.get("experience_years", 0)
    if "1-10" in company_size or "startup" in company_size.lower():
        size_score = 90 if exp < 5 else 70  # Startups prefer dynamic early-career
    elif "500+" in company_size or "1000+" in company_size:
        size_score = 85 if exp > 3 else 65  # Large companies prefer experience
    scores["size_fit"] = size_score

    # 5. Location Fit
    location_score = 60
    user_loc = (user_data.get("preferred_location") or "").lower()
    company_hq = (company_data.get("headquarters") or "").lower()
    company_locs = [l.lower() for l in (company_data.get("locations") or [])]

    if user_loc:
        if user_loc in company_hq or company_hq in user_loc:
            location_score = 100
        elif any(user_loc in loc or loc in user_loc for loc in company_locs):
            location_score = 90
        elif user_data.get("work_mode") == "remote":
            location_score = 80
    scores["location_fit"] = location_score

    # Overall
    weights = {"technical_fit": 0.35, "culture_fit": 0.20, "industry_fit": 0.15, "size_fit": 0.10, "location_fit": 0.20}
    overall = sum(scores[k] * weights[k] for k in weights)
    scores["overall_fit"] = round(overall, 1)

    # Recommendation
    if overall >= 80:
        recommendation = "🟢 Excellent fit! This company aligns very well with your profile."
    elif overall >= 60:
        recommendation = "🟡 Good fit with some areas to explore. Consider researching their culture more."
    else:
        recommendation = "🔴 Moderate fit. There may be gaps in alignment. Review carefully."

    return {
        "scores": scores,
        "recommendation": recommendation,
        "matching_tech": list(user_skills & company_tech) if company_tech else [],
        "missing_tech": list(company_tech - user_skills) if company_tech else [],
        "insights": _generate_insights(scores, user_data, company_data),
    }


def predict_company_fit_with_llm(user_data: dict, company_data: dict) -> dict:
    """LLM-powered company fit analysis."""
    from services.llm_service import get_llm
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a career advisor analyzing company-candidate fit.
Return a JSON object:
{{
    "overall_fit_pct": 75,
    "dimensions": {{
        "technical": {{"score": 80, "reason": "..."}},
        "culture": {{"score": 70, "reason": "..."}},
        "growth": {{"score": 85, "reason": "..."}},
        "compensation": {{"score": 60, "reason": "..."}},
        "work_life_balance": {{"score": 75, "reason": "..."}}
    }},
    "pros": ["Pro 1", "Pro 2"],
    "cons": ["Con 1"],
    "recommendation": "Overall recommendation",
    "questions_to_ask": ["Question to ask during interview"]
}}
Return ONLY valid JSON."""),
        ("human", """Candidate: Skills={skills}, Experience={exp}yr, Preference={pref}
Company: {company_name}, Industry={industry}, Size={size}, Tech={tech}""")
    ])

    try:
        llm = get_llm()
        chain = prompt | llm
        response = chain.invoke({
            "skills": ", ".join((user_data.get("technical_skills") or [])[:10]),
            "exp": user_data.get("experience_years", 0),
            "pref": user_data.get("preferred_role", ""),
            "company_name": company_data.get("name", ""),
            "industry": company_data.get("industry", ""),
            "size": company_data.get("company_size", ""),
            "tech": ", ".join((company_data.get("tech_stack") or [])[:10]),
        })
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        return predict_company_fit(user_data, company_data)


def _generate_insights(scores: dict, user_data: dict, company_data: dict) -> list[str]:
    """Generate human-readable insights from scores."""
    insights = []
    if scores["technical_fit"] >= 80:
        insights.append("✅ Strong technical alignment with the company's stack")
    elif scores["technical_fit"] < 50:
        insights.append("⚠️ Technical skill gap — consider upskilling in their tech stack")

    if scores["culture_fit"] >= 80:
        insights.append("✅ Work culture preferences match well")
    if scores["location_fit"] >= 90:
        insights.append("✅ Location is a great match")
    elif scores["location_fit"] < 50:
        insights.append("⚠️ Location may require relocation or remote arrangements")

    if scores["overall_fit"] >= 75:
        insights.append("🎯 Overall strong candidate for this company")
    return insights
