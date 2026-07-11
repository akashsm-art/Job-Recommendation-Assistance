"""
TalentSpark AI — AI Resume Writer & Cover Letter Generator
Rewrites resumes for specific roles and generates tailored cover letters.
"""

import json


def rewrite_resume(resume_text: str, target_role: str, job_description: str = None) -> dict:
    """
    AI-powered resume rewriting optimized for a specific role.
    Returns rewritten sections with ATS-optimized content.
    """
    from services.llm_service import get_llm
    from langchain_core.prompts import ChatPromptTemplate

    jd_context = f"\nTarget Job Description:\n{job_description}" if job_description else ""

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert resume writer and ATS optimization specialist.
Rewrite the given resume to be optimized for the target role.
{jd_context}

Return a valid JSON object:
{{
    "professional_summary": "A compelling 3-4 sentence professional summary",
    "key_highlights": ["Achievement 1 with metrics", "Achievement 2", "Achievement 3"],
    "optimized_skills": {{
        "technical": ["Skill1", "Skill2"],
        "tools": ["Tool1", "Tool2"],
        "soft": ["Communication", "Leadership"]
    }},
    "experience_bullets": [
        "• Developed X using Y, resulting in Z% improvement",
        "• Led team of N engineers to deliver ..."
    ],
    "keywords_added": ["keyword1", "keyword2"],
    "ats_tips": ["Tip 1", "Tip 2"],
    "before_after": [
        {{"before": "Worked on projects", "after": "Spearheaded 5+ cross-functional projects, reducing deployment time by 40%"}}
    ],
    "overall_improvement": "Brief summary of improvements made"
}}
Make achievements specific and quantifiable. Return ONLY valid JSON."""),
        ("human", """Resume to optimize:
{resume_text}

Target Role: {target_role}""")
    ])

    try:
        llm = get_llm()
        chain = prompt | llm
        response = chain.invoke({
            "resume_text": resume_text,
            "target_role": target_role,
            "jd_context": jd_context,
        })
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        print(f"[Resume Writer] LLM failed: {e}")
        return _fallback_rewrite(resume_text, target_role)


def generate_cover_letter(
    user_name: str,
    target_role: str,
    company_name: str,
    user_skills: list[str],
    experience_years: float,
    resume_text: str = None,
    job_description: str = None,
    tone: str = "professional",
) -> dict:
    """
    Generate a tailored cover letter for a specific job application.
    """
    from services.llm_service import get_llm
    from langchain_core.prompts import ChatPromptTemplate

    jd_context = f"\nJob Description:\n{job_description}" if job_description else ""
    resume_context = f"\nCandidate Resume:\n{resume_text[:2000]}" if resume_text else ""

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert cover letter writer.
Write a compelling, personalized cover letter for the given job application.
Tone: {tone}
{jd_context}
{resume_context}

Return a valid JSON object:
{{
    "cover_letter": "Full cover letter text (3-4 paragraphs, well-formatted)",
    "subject_line": "Email subject line for the application",
    "key_selling_points": ["Point 1", "Point 2", "Point 3"],
    "personalization_tips": ["How to further personalize this letter"],
    "word_count": 250
}}
Return ONLY valid JSON."""),
        ("human", """Candidate: {name}
Target Role: {role}
Company: {company}
Key Skills: {skills}
Experience: {experience} years""")
    ])

    try:
        llm = get_llm()
        chain = prompt | llm
        response = chain.invoke({
            "name": user_name,
            "role": target_role,
            "company": company_name,
            "skills": ", ".join(user_skills[:10]),
            "experience": experience_years,
            "tone": tone,
            "jd_context": jd_context,
            "resume_context": resume_context,
        })
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        print(f"[Cover Letter] LLM failed: {e}")
        return _fallback_cover_letter(user_name, target_role, company_name, user_skills, experience_years)


def _fallback_rewrite(resume_text: str, target_role: str) -> dict:
    """Fallback resume rewrite without LLM."""
    return {
        "professional_summary": (
            f"Results-driven professional seeking a {target_role} role. "
            "Bringing strong technical skills and a passion for building high-quality solutions."
        ),
        "key_highlights": [
            "Proficient in modern development technologies and best practices",
            "Strong problem-solving abilities with attention to detail",
            "Experience in collaborative, agile team environments",
        ],
        "optimized_skills": {
            "technical": ["Python", "JavaScript", "SQL"],
            "tools": ["Git", "Docker", "VS Code"],
            "soft": ["Communication", "Problem Solving", "Teamwork"],
        },
        "experience_bullets": [
            "• Developed and maintained software applications using modern tech stack",
            "• Collaborated with cross-functional teams to deliver projects on time",
            "• Implemented best practices for code quality and testing",
        ],
        "keywords_added": [target_role.lower(), "agile", "scalable", "production"],
        "ats_tips": [
            "Use standard section headers (Experience, Education, Skills)",
            "Include specific metrics and achievements",
            "Mirror keywords from the job description",
            "Use a clean, single-column format",
        ],
        "before_after": [],
        "overall_improvement": "Resume structure optimized for ATS compatibility (local engine)",
    }


def _fallback_cover_letter(name: str, role: str, company: str, skills: list[str], exp: float) -> dict:
    """Fallback cover letter generation."""
    skills_text = ", ".join(skills[:5]) if skills else "relevant technical skills"
    letter = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {role} position at {company}. With {exp:.0f} years of experience and expertise in {skills_text}, I am confident in my ability to make a meaningful contribution to your team.

Throughout my career, I have developed a strong foundation in software development, consistently delivering high-quality solutions that meet business objectives. My technical proficiency, combined with excellent communication skills and a collaborative mindset, enables me to work effectively in fast-paced environments.

I am particularly drawn to {company}'s commitment to innovation and would welcome the opportunity to bring my skills and passion to your organization. I am eager to discuss how my background aligns with your team's needs.

Thank you for considering my application. I look forward to the possibility of contributing to {company}'s continued success.

Best regards,
{name}"""

    return {
        "cover_letter": letter,
        "subject_line": f"Application for {role} - {name}",
        "key_selling_points": [
            f"{exp:.0f} years of relevant experience",
            f"Proficiency in {skills_text}",
            "Strong communication and collaboration skills",
        ],
        "personalization_tips": [
            "Research the company's recent projects and mention them",
            "Reference specific team members or company values",
            "Include a specific achievement relevant to the role",
        ],
        "word_count": len(letter.split()),
    }
