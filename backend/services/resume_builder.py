"""
TalentSpark AI — AI Resume Builder
Generate professional resumes from structured data with multiple templates.
"""

import json
from datetime import datetime


RESUME_TEMPLATES = {
    "modern": {
        "name": "Modern Professional",
        "description": "Clean, modern design with accent colors and clear sections",
        "style": "modern",
    },
    "minimal": {
        "name": "Minimal Clean",
        "description": "Simple, elegant design focusing on content clarity",
        "style": "minimal",
    },
    "corporate": {
        "name": "Corporate Executive",
        "description": "Formal, structured layout suitable for enterprise roles",
        "style": "corporate",
    },
    "ats_friendly": {
        "name": "ATS Optimized",
        "description": "Maximum ATS compatibility with standard formatting",
        "style": "ats_friendly",
    },
}


def generate_resume_content(user_data: dict, target_role: str = None, template: str = "modern") -> dict:
    """Generate professional resume content from user data."""

    # Build structured resume sections
    resume = {
        "template": RESUME_TEMPLATES.get(template, RESUME_TEMPLATES["modern"]),
        "generated_at": datetime.now().isoformat(),
        "sections": {},
    }

    # Header
    resume["sections"]["header"] = {
        "name": user_data.get("full_name", "Your Name"),
        "title": target_role or user_data.get("preferred_role", "Software Professional"),
        "email": user_data.get("email", ""),
        "phone": user_data.get("phone", ""),
        "location": user_data.get("preferred_location", ""),
        "linkedin": user_data.get("linkedin", ""),
        "github": user_data.get("github", ""),
        "portfolio": user_data.get("portfolio", ""),
    }

    # Professional Summary
    resume["sections"]["summary"] = _generate_summary(user_data, target_role)

    # Skills
    resume["sections"]["skills"] = {
        "technical": user_data.get("technical_skills", []),
        "programming_languages": user_data.get("programming_languages", []),
        "frameworks": user_data.get("frameworks", []),
        "databases": user_data.get("databases_known", []),
        "cloud": user_data.get("cloud_skills", []),
        "tools": user_data.get("ai_skills", []),
        "soft_skills": user_data.get("soft_skills", []),
    }

    # Experience
    resume["sections"]["experience"] = user_data.get("experience_records", [])

    # Education
    resume["sections"]["education"] = user_data.get("education_records", [])

    # Projects
    resume["sections"]["projects"] = user_data.get("projects", [])

    # Certifications
    resume["sections"]["certifications"] = user_data.get("certificates", [])

    return resume


def generate_resume_html(user_data: dict, template: str = "modern", target_role: str = None) -> str:
    """Generate a complete HTML resume ready for PDF conversion."""

    name = user_data.get("full_name", "Your Name")
    role = target_role or user_data.get("preferred_role", "Software Professional")
    email = user_data.get("email", "")
    phone = user_data.get("phone", "")
    location = user_data.get("preferred_location", "")
    linkedin = user_data.get("linkedin", "")
    github = user_data.get("github", "")

    # Skills
    all_skills = []
    for key in ["technical_skills", "programming_languages", "frameworks", "databases_known", "cloud_skills"]:
        all_skills.extend(user_data.get(key) or [])
    skills_html = " • ".join(all_skills[:20]) if all_skills else "Add your skills"

    # Summary
    summary = _generate_summary(user_data, target_role)

    # Experience
    exp_html = ""
    for exp in (user_data.get("experience_records") or []):
        if isinstance(exp, dict):
            exp_html += f"""
            <div class="entry">
                <div class="entry-header">
                    <strong>{exp.get('role', 'Role')}</strong> — {exp.get('company', 'Company')}
                    <span class="date">{exp.get('start_date', '')} — {exp.get('end_date', 'Present')}</span>
                </div>
                <p>{exp.get('description', '')}</p>
            </div>"""

    # Education
    edu_html = ""
    for edu in (user_data.get("education_records") or []):
        if isinstance(edu, dict):
            edu_html += f"""
            <div class="entry">
                <strong>{edu.get('degree', 'Degree')}</strong> — {edu.get('institution', 'University')}
                <span class="date">{edu.get('end_year', '')}</span>
                {f'<p>CGPA: {edu["cgpa"]}</p>' if edu.get('cgpa') else ''}
            </div>"""

    # Projects
    proj_html = ""
    for proj in (user_data.get("projects") or []):
        if isinstance(proj, dict):
            tech = ", ".join(proj.get("tech_stack") or [])
            proj_html += f"""
            <div class="entry">
                <strong>{proj.get('title', 'Project')}</strong>
                {f'<span class="tech">[{tech}]</span>' if tech else ''}
                <p>{proj.get('description', '')}</p>
            </div>"""

    # Template styles
    colors = {
        "modern": {"primary": "#667eea", "secondary": "#764ba2", "bg": "#f8fafc"},
        "minimal": {"primary": "#1a1a2e", "secondary": "#16213e", "bg": "#ffffff"},
        "corporate": {"primary": "#0f4c75", "secondary": "#1b262c", "bg": "#f5f5f5"},
        "ats_friendly": {"primary": "#000000", "secondary": "#333333", "bg": "#ffffff"},
    }
    c = colors.get(template, colors["modern"])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{name} — Resume</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, sans-serif; color: #333; background: {c['bg']}; line-height: 1.6; }}
    .resume {{ max-width: 800px; margin: 20px auto; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
    .header {{ background: linear-gradient(135deg, {c['primary']}, {c['secondary']}); color: white; padding: 40px; text-align: center; }}
    .header h1 {{ font-size: 28px; margin-bottom: 5px; letter-spacing: 1px; }}
    .header .role {{ font-size: 16px; opacity: 0.9; margin-bottom: 15px; }}
    .header .contact {{ font-size: 13px; opacity: 0.85; }}
    .header .contact span {{ margin: 0 10px; }}
    .content {{ padding: 30px 40px; }}
    .section {{ margin-bottom: 25px; }}
    .section h2 {{ color: {c['primary']}; font-size: 16px; text-transform: uppercase; letter-spacing: 2px; border-bottom: 2px solid {c['primary']}; padding-bottom: 5px; margin-bottom: 12px; }}
    .entry {{ margin-bottom: 12px; }}
    .entry-header {{ display: flex; justify-content: space-between; align-items: baseline; }}
    .date {{ color: #888; font-size: 13px; }}
    .tech {{ color: {c['primary']}; font-size: 13px; }}
    .skills {{ font-size: 14px; line-height: 1.8; }}
    p {{ font-size: 14px; color: #555; margin-top: 4px; }}
    .summary {{ font-size: 14px; color: #555; font-style: italic; }}
</style>
</head>
<body>
<div class="resume">
    <div class="header">
        <h1>{name}</h1>
        <div class="role">{role}</div>
        <div class="contact">
            {f'<span>📧 {email}</span>' if email else ''}
            {f'<span>📱 {phone}</span>' if phone else ''}
            {f'<span>📍 {location}</span>' if location else ''}
            {f'<span>🔗 {linkedin}</span>' if linkedin else ''}
            {f'<span>💻 {github}</span>' if github else ''}
        </div>
    </div>
    <div class="content">
        <div class="section">
            <h2>Professional Summary</h2>
            <p class="summary">{summary}</p>
        </div>
        <div class="section">
            <h2>Technical Skills</h2>
            <p class="skills">{skills_html}</p>
        </div>
        {f'<div class="section"><h2>Experience</h2>{exp_html}</div>' if exp_html else ''}
        {f'<div class="section"><h2>Education</h2>{edu_html}</div>' if edu_html else ''}
        {f'<div class="section"><h2>Projects</h2>{proj_html}</div>' if proj_html else ''}
    </div>
</div>
</body>
</html>"""

    return html


def _generate_summary(user_data: dict, target_role: str = None) -> str:
    """Generate a professional summary."""
    role = target_role or user_data.get("preferred_role", "Software Professional")
    exp = user_data.get("experience_years", 0)
    skills = (user_data.get("technical_skills") or [])[:5]

    if exp > 0:
        return (
            f"Results-driven {role} with {exp:.0f}+ years of experience in "
            f"{', '.join(skills[:3]) if skills else 'software development'}. "
            f"Passionate about building scalable solutions and leveraging cutting-edge technologies "
            f"to solve complex business challenges."
        )
    return (
        f"Motivated {role} with strong foundations in "
        f"{', '.join(skills[:3]) if skills else 'software development'}. "
        f"Eager to apply technical skills and creative problem-solving abilities "
        f"in a collaborative, growth-oriented environment."
    )


def get_available_templates() -> list[dict]:
    """Get all available resume templates."""
    return [{"id": k, **v} for k, v in RESUME_TEMPLATES.items()]
