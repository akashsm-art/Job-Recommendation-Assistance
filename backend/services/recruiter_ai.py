"""
TalentSpark AI — AI Recruiter Assistant
Candidate ranking, duplicate detection, and recruiter AI tools.
"""

import json
from typing import Optional


def rank_candidates_for_job(job_data: dict, candidates: list[dict]) -> list[dict]:
    """
    AI-powered candidate ranking for a job.
    Ranks candidates by multi-factor match scoring.
    """
    from services.similarity import calculate_comprehensive_match

    ranked = []
    for candidate in candidates:
        match = calculate_comprehensive_match(candidate, job_data)
        ranked.append({
            "user_id": candidate.get("id"),
            "name": candidate.get("full_name", "Unknown"),
            "email": candidate.get("email", ""),
            "match_score": match["overall_match"],
            "technical_match": match["technical_match"],
            "experience_match": match["experience_match"],
            "education_match": match["education_match"],
            "matching_skills": match["matching_skills"],
            "missing_skills": match["missing_skills"],
            "rank_reason": _generate_rank_reason(match),
        })

    ranked.sort(key=lambda x: x["match_score"], reverse=True)

    # Assign ranks
    for i, candidate in enumerate(ranked, 1):
        candidate["rank"] = i
        if candidate["match_score"] >= 80:
            candidate["tier"] = "🟢 Top Match"
        elif candidate["match_score"] >= 60:
            candidate["tier"] = "🟡 Good Match"
        else:
            candidate["tier"] = "🔴 Partial Match"

    return ranked


def detect_duplicate_resumes(resume_text_1: str, resume_text_2: str) -> dict:
    """
    Detect if two resumes are duplicates or highly similar.
    Uses text similarity and structural comparison.
    """
    from services.embeddings import embed_text
    import numpy as np

    # Embed both resumes
    vec1 = np.array(embed_text(resume_text_1))
    vec2 = np.array(embed_text(resume_text_2))

    # Cosine similarity
    cosine_sim = float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))

    # Text overlap
    words1 = set(resume_text_1.lower().split())
    words2 = set(resume_text_2.lower().split())
    jaccard = len(words1 & words2) / max(len(words1 | words2), 1)

    # Combined score
    similarity = cosine_sim * 0.6 + jaccard * 0.4
    is_duplicate = similarity > 0.85

    return {
        "similarity_score": round(similarity * 100, 1),
        "cosine_similarity": round(cosine_sim * 100, 1),
        "text_overlap_pct": round(jaccard * 100, 1),
        "is_duplicate": is_duplicate,
        "verdict": "🔴 Likely Duplicate" if is_duplicate else (
            "🟡 Partially Similar" if similarity > 0.6 else "🟢 Unique"
        ),
    }


def analyze_resume_authenticity(resume_text: str) -> dict:
    """
    AI-powered fake resume detection.
    Checks for red flags and inconsistencies.
    """
    import re
    text = resume_text
    text_lower = text.lower()
    flags = []
    score = 100  # Start with perfect, deduct for issues

    # Check 1: Unrealistic experience claims
    years_matches = re.findall(r'(\d+)\+?\s*(?:years?|yrs?)', text_lower)
    if years_matches:
        max_years = max(int(y) for y in years_matches)
        if max_years > 30:
            flags.append("⚠️ Unusually high experience claim (>30 years)")
            score -= 15

    # Check 2: Too many skills (skill stuffing)
    skill_count = text_lower.count(',') + text_lower.count('•') + text_lower.count('●')
    if skill_count > 80:
        flags.append("⚠️ Possible skill stuffing (excessive number of listed items)")
        score -= 10

    # Check 3: Missing contact info
    has_email = bool(re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text))
    has_phone = bool(re.search(r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\./0-9]{7,15}', text))
    if not has_email:
        flags.append("⚠️ No email address found")
        score -= 10
    if not has_phone:
        flags.append("⚠️ No phone number found")
        score -= 5

    # Check 4: Generic/template text
    generic_phrases = [
        "hardworking individual", "team player with excellent", "passionate about",
        "results-oriented", "self-motivated professional", "proven track record",
    ]
    generic_count = sum(1 for p in generic_phrases if p in text_lower)
    if generic_count >= 3:
        flags.append("⚠️ Heavy use of generic phrases (may be template-based)")
        score -= 10

    # Check 5: Very short resume
    word_count = len(text.split())
    if word_count < 50:
        flags.append("⚠️ Resume is too short to be comprehensive")
        score -= 20
    elif word_count < 150:
        flags.append("ℹ️ Resume could be more detailed")
        score -= 5

    # Check 6: Inconsistent dates
    date_patterns = re.findall(r'20[0-2]\d', text)
    if date_patterns:
        years = sorted(set(int(y) for y in date_patterns))
        if years and years[-1] > 2026:
            flags.append("⚠️ Future dates detected")
            score -= 15

    # Check 7: No verifiable links
    has_linkedin = "linkedin" in text_lower
    has_github = "github" in text_lower
    if not has_linkedin and not has_github:
        flags.append("ℹ️ No LinkedIn or GitHub profile links found")
        score -= 5

    score = max(0, score)

    if score >= 85:
        verdict = "🟢 Appears Authentic"
    elif score >= 60:
        verdict = "🟡 Minor Concerns"
    else:
        verdict = "🔴 Significant Red Flags"

    return {
        "authenticity_score": score,
        "verdict": verdict,
        "flags": flags,
        "word_count": word_count,
        "has_contact_info": has_email and has_phone,
        "has_verifiable_links": has_linkedin or has_github,
        "recommendations": [
            "Verify contact information independently",
            "Cross-reference LinkedIn profile",
            "Validate employment history during interview",
        ] if score < 85 else ["Resume passes basic authenticity checks"],
    }


def generate_recruiter_summary(job_data: dict, applicants_data: list[dict]) -> dict:
    """Generate an AI summary for recruiters about their job posting's applicants."""
    total = len(applicants_data)
    if total == 0:
        return {"summary": "No applications received yet.", "stats": {}}

    scores = [a.get("match_score", 0) for a in applicants_data if a.get("match_score")]
    avg_score = sum(scores) / max(len(scores), 1) if scores else 0

    top_matches = sum(1 for s in scores if s >= 80)
    good_matches = sum(1 for s in scores if 60 <= s < 80)
    low_matches = sum(1 for s in scores if s < 60)

    # Skill distribution
    all_skills = []
    for app in applicants_data:
        all_skills.extend(app.get("matching_skills", []))
    skill_freq = {}
    for s in all_skills:
        skill_freq[s] = skill_freq.get(s, 0) + 1
    top_skills = sorted(skill_freq.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "summary": (
            f"📊 Received {total} applications with an average match score of {avg_score:.0f}%. "
            f"{top_matches} top matches (80%+), {good_matches} good matches (60-80%), "
            f"and {low_matches} below threshold."
        ),
        "stats": {
            "total_applicants": total,
            "avg_match_score": round(avg_score, 1),
            "top_matches": top_matches,
            "good_matches": good_matches,
            "low_matches": low_matches,
        },
        "top_skills_in_pool": [{"skill": s, "count": c} for s, c in top_skills],
        "recommendation": (
            "🟢 Strong applicant pool — review top matches first"
            if top_matches >= 3 else (
                "🟡 Moderate pool — consider broadening the search"
                if good_matches >= 3 else
                "🔴 Weak applicant pool — consider revising job requirements"
            )
        ),
    }


def _generate_rank_reason(match: dict) -> str:
    """Generate a human-readable ranking reason."""
    reasons = []
    if match["technical_match"] >= 80:
        reasons.append("Strong technical fit")
    if match["experience_match"] >= 80:
        reasons.append("Excellent experience match")
    if match.get("matching_skills"):
        reasons.append(f"Matches {len(match['matching_skills'])} required skills")
    if match.get("missing_skills"):
        reasons.append(f"Missing {len(match['missing_skills'])} skills")
    return " | ".join(reasons) if reasons else "General profile match"
