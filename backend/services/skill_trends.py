"""
TalentSpark AI — Skill Trends & Job Market Analysis
AI-powered skill demand analysis and market trend insights.
"""

import json
from datetime import datetime


# Skill trend data (2024-2025 market intelligence)
SKILL_TRENDS = {
    "python": {"demand": "Very High", "trend": "📈 Rising", "growth_pct": 25, "avg_salary_boost_pct": 15, "category": "Programming"},
    "javascript": {"demand": "Very High", "trend": "➡️ Stable", "growth_pct": 10, "avg_salary_boost_pct": 12, "category": "Programming"},
    "typescript": {"demand": "High", "trend": "📈 Rising Fast", "growth_pct": 40, "avg_salary_boost_pct": 18, "category": "Programming"},
    "rust": {"demand": "Growing", "trend": "📈 Rising Fast", "growth_pct": 65, "avg_salary_boost_pct": 25, "category": "Programming"},
    "golang": {"demand": "High", "trend": "📈 Rising", "growth_pct": 30, "avg_salary_boost_pct": 20, "category": "Programming"},
    "react": {"demand": "Very High", "trend": "➡️ Stable", "growth_pct": 8, "avg_salary_boost_pct": 14, "category": "Frontend"},
    "next.js": {"demand": "High", "trend": "📈 Rising Fast", "growth_pct": 50, "avg_salary_boost_pct": 18, "category": "Frontend"},
    "vue": {"demand": "Moderate", "trend": "➡️ Stable", "growth_pct": 5, "avg_salary_boost_pct": 10, "category": "Frontend"},
    "angular": {"demand": "Moderate", "trend": "📉 Declining", "growth_pct": -5, "avg_salary_boost_pct": 8, "category": "Frontend"},
    "fastapi": {"demand": "High", "trend": "📈 Rising Fast", "growth_pct": 55, "avg_salary_boost_pct": 16, "category": "Backend"},
    "django": {"demand": "Moderate", "trend": "➡️ Stable", "growth_pct": 3, "avg_salary_boost_pct": 10, "category": "Backend"},
    "node.js": {"demand": "High", "trend": "➡️ Stable", "growth_pct": 8, "avg_salary_boost_pct": 12, "category": "Backend"},
    "docker": {"demand": "Very High", "trend": "📈 Rising", "growth_pct": 20, "avg_salary_boost_pct": 18, "category": "DevOps"},
    "kubernetes": {"demand": "Very High", "trend": "📈 Rising", "growth_pct": 30, "avg_salary_boost_pct": 25, "category": "DevOps"},
    "terraform": {"demand": "High", "trend": "📈 Rising", "growth_pct": 35, "avg_salary_boost_pct": 22, "category": "DevOps"},
    "aws": {"demand": "Very High", "trend": "📈 Rising", "growth_pct": 22, "avg_salary_boost_pct": 20, "category": "Cloud"},
    "gcp": {"demand": "High", "trend": "📈 Rising", "growth_pct": 28, "avg_salary_boost_pct": 20, "category": "Cloud"},
    "azure": {"demand": "High", "trend": "📈 Rising", "growth_pct": 25, "avg_salary_boost_pct": 18, "category": "Cloud"},
    "machine learning": {"demand": "Very High", "trend": "📈 Rising Fast", "growth_pct": 45, "avg_salary_boost_pct": 30, "category": "AI/ML"},
    "deep learning": {"demand": "High", "trend": "📈 Rising", "growth_pct": 35, "avg_salary_boost_pct": 28, "category": "AI/ML"},
    "langchain": {"demand": "High", "trend": "🚀 Explosive Growth", "growth_pct": 200, "avg_salary_boost_pct": 35, "category": "AI/ML"},
    "llm": {"demand": "Very High", "trend": "🚀 Explosive Growth", "growth_pct": 300, "avg_salary_boost_pct": 40, "category": "AI/ML"},
    "rag": {"demand": "High", "trend": "🚀 Explosive Growth", "growth_pct": 250, "avg_salary_boost_pct": 35, "category": "AI/ML"},
    "prompt engineering": {"demand": "High", "trend": "🚀 Explosive Growth", "growth_pct": 400, "avg_salary_boost_pct": 30, "category": "AI/ML"},
    "postgresql": {"demand": "High", "trend": "📈 Rising", "growth_pct": 15, "avg_salary_boost_pct": 10, "category": "Database"},
    "mongodb": {"demand": "Moderate", "trend": "➡️ Stable", "growth_pct": 5, "avg_salary_boost_pct": 8, "category": "Database"},
    "redis": {"demand": "High", "trend": "📈 Rising", "growth_pct": 20, "avg_salary_boost_pct": 12, "category": "Database"},
    "graphql": {"demand": "Moderate", "trend": "📈 Rising", "growth_pct": 18, "avg_salary_boost_pct": 12, "category": "API"},
    "cybersecurity": {"demand": "Very High", "trend": "📈 Rising Fast", "growth_pct": 35, "avg_salary_boost_pct": 25, "category": "Security"},
}

JOB_MARKET_TRENDS = {
    "remote_work": {"status": "📈 Growing", "pct_remote_jobs": 35, "insight": "Remote jobs increasing but companies are pushing for hybrid."},
    "ai_adoption": {"status": "🚀 Explosive", "pct_ai_jobs": 15, "insight": "AI/ML roles have tripled in 2 years. LLM expertise is the hottest skill."},
    "startup_hiring": {"status": "📊 Moderate", "insight": "Startups are hiring selectively, focusing on full-stack and AI roles."},
    "big_tech": {"status": "➡️ Stable", "insight": "FAANG companies have stabilized hiring after 2023 layoffs."},
    "salary_trends": {"status": "📈 Rising", "avg_hike_pct": 12, "insight": "Average salary hikes are 10-15% for in-demand skills."},
    "freelance": {"status": "📈 Growing", "insight": "Freelance tech work growing, especially in AI, web development, and DevOps."},
}


def get_skill_trends(skills: list[str] = None) -> dict:
    """Get market trends for specific skills or all tracked skills."""
    if skills:
        result = {}
        for skill in skills:
            skill_lower = skill.lower().strip()
            if skill_lower in SKILL_TRENDS:
                result[skill] = SKILL_TRENDS[skill_lower]
            else:
                # Try partial match
                for key, data in SKILL_TRENDS.items():
                    if key in skill_lower or skill_lower in key:
                        result[skill] = data
                        break
                if skill not in result:
                    result[skill] = {"demand": "Unknown", "trend": "❓ No data", "growth_pct": 0}
        return {"skills": result, "updated": datetime.now().isoformat()}

    # Return all trends grouped by category
    categories = {}
    for skill, data in SKILL_TRENDS.items():
        cat = data.get("category", "Other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append({"skill": skill.title(), **data})

    return {"categories": categories, "updated": datetime.now().isoformat()}


def get_job_market_overview() -> dict:
    """Get overall job market trends and insights."""
    return {
        "trends": JOB_MARKET_TRENDS,
        "top_growing_skills": _get_top_growing(),
        "hot_roles": [
            {"role": "AI/ML Engineer", "demand": "🔥 Extremely High", "avg_salary": "18-50 LPA", "openings_trend": "+150%"},
            {"role": "Full Stack Developer", "demand": "🔥 Very High", "avg_salary": "10-35 LPA", "openings_trend": "+20%"},
            {"role": "DevOps/Cloud Engineer", "demand": "🔥 Very High", "avg_salary": "12-40 LPA", "openings_trend": "+35%"},
            {"role": "Data Scientist", "demand": "📈 High", "avg_salary": "12-45 LPA", "openings_trend": "+25%"},
            {"role": "Cybersecurity Analyst", "demand": "📈 High", "avg_salary": "10-35 LPA", "openings_trend": "+40%"},
            {"role": "Product Manager", "demand": "📈 High", "avg_salary": "15-50 LPA", "openings_trend": "+15%"},
        ],
        "insights": [
            "🤖 AI/LLM skills have become the #1 differentiator in tech hiring",
            "☁️ Cloud certifications (AWS/GCP) significantly boost salary offers",
            "🔄 Full-stack skills remain the most versatile career path",
            "🛡️ Cybersecurity demand is outpacing supply — great career opportunity",
            "📱 Mobile development is stable but growth has slowed",
        ],
        "updated": datetime.now().isoformat(),
    }


def analyze_user_skill_market_value(user_skills: list[str]) -> dict:
    """Analyze the market value of a user's skill set."""
    if not user_skills:
        return {"message": "No skills provided for analysis"}

    trending = []
    declining = []
    stable = []
    unknown = []
    total_boost = 0

    for skill in user_skills:
        skill_lower = skill.lower().strip()
        if skill_lower in SKILL_TRENDS:
            data = SKILL_TRENDS[skill_lower]
            entry = {"skill": skill, **data}
            total_boost += data.get("avg_salary_boost_pct", 0)

            if data["growth_pct"] > 20:
                trending.append(entry)
            elif data["growth_pct"] < 0:
                declining.append(entry)
            else:
                stable.append(entry)
        else:
            unknown.append(skill)

    return {
        "trending_skills": sorted(trending, key=lambda x: x["growth_pct"], reverse=True),
        "stable_skills": stable,
        "declining_skills": declining,
        "untracked_skills": unknown,
        "estimated_salary_boost_pct": round(total_boost / max(len(user_skills), 1), 1),
        "market_readiness": _calculate_market_readiness(trending, stable, declining, user_skills),
        "recommendations": _generate_skill_recommendations(trending, declining, unknown),
    }


def _get_top_growing() -> list:
    """Get top 10 fastest growing skills."""
    sorted_skills = sorted(SKILL_TRENDS.items(), key=lambda x: x[1]["growth_pct"], reverse=True)
    return [{"skill": k.title(), **v} for k, v in sorted_skills[:10]]


def _calculate_market_readiness(trending, stable, declining, all_skills) -> dict:
    """Calculate overall market readiness score."""
    total = max(len(all_skills), 1)
    trending_pct = (len(trending) / total) * 100
    declining_pct = (len(declining) / total) * 100

    score = min(100, 50 + trending_pct - declining_pct * 2)
    level = "🟢 Excellent" if score >= 80 else "🟡 Good" if score >= 60 else "🔴 Needs Improvement"

    return {"score": round(score), "level": level, "trending_pct": round(trending_pct), "declining_pct": round(declining_pct)}


def _generate_skill_recommendations(trending, declining, unknown) -> list:
    """Generate actionable skill recommendations."""
    recs = []
    if not trending:
        recs.append("🚀 Consider learning AI/ML or Cloud skills — they have the highest growth")
    if declining:
        names = ", ".join(d["skill"] for d in declining[:3])
        recs.append(f"⚠️ Skills like {names} are declining — consider complementing with modern alternatives")
    if len(trending) >= 3:
        recs.append("✅ Great portfolio of trending skills — keep building projects to showcase them")
    recs.append("💡 Tip: Combine skills (e.g., Python + LLM + Cloud) for maximum market value")
    return recs
