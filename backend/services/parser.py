"""
TalentSpark AI — Resume Parser Service
Parse PDF, DOCX, and TXT resumes to extract structured data.
Uses LLM for intelligent extraction with regex fallback.
"""

import re
import json
from typing import Optional
from pathlib import Path


def parse_pdf(file_path: str) -> str:
    """Extract text from a PDF file using PyMuPDF."""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        print(f"[Parser] PDF parsing error: {e}")
        return ""


def parse_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    try:
        from docx import Document
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        print(f"[Parser] DOCX parsing error: {e}")
        return ""


def parse_txt(file_path: str) -> str:
    """Read a plain text file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        print(f"[Parser] TXT parsing error: {e}")
        return ""


def parse_resume_file(file_path: str) -> str:
    """Parse a resume file based on its extension."""
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return parse_pdf(file_path)
    elif ext == ".docx":
        return parse_docx(file_path)
    elif ext == ".txt":
        return parse_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}. Supported: .pdf, .docx, .txt")


def extract_resume_data_with_llm(resume_text: str) -> dict:
    """
    Use LLM to extract structured data from resume text.
    Returns a dict with: name, email, phone, skills, education, experience, etc.
    """
    from services.llm_service import get_llm
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional resume parser. Extract structured data from the resume text.
Return a valid JSON object with these exact keys:
{{
    "full_name": "string or null",
    "email": "string or null",
    "phone": "string or null",
    "skills": ["list", "of", "skills"],
    "technical_skills": ["Python", "React", ...],
    "soft_skills": ["Communication", ...],
    "programming_languages": ["Python", "JavaScript", ...],
    "frameworks": ["FastAPI", "React", ...],
    "databases": ["PostgreSQL", "MongoDB", ...],
    "cloud_skills": ["AWS", "GCP", ...],
    "ai_skills": ["Machine Learning", ...],
    "education": [
        {{"degree": "B.Tech", "field": "CS", "institution": "MIT", "year": 2024, "cgpa": 8.5}}
    ],
    "experience": [
        {{"company": "Google", "role": "SDE", "duration": "2 years", "description": "..."}}
    ],
    "projects": [
        {{"title": "Project Name", "description": "...", "tech_stack": ["Python"]}}
    ],
    "certifications": ["AWS Certified", "..."],
    "links": ["linkedin.com/...", "github.com/..."],
    "languages": ["English", "Hindi"],
    "summary": "Brief professional summary"
}}
Return ONLY valid JSON, no markdown or extra text."""),
        ("human", "{resume_text}")
    ])

    try:
        llm = get_llm()
        chain = prompt | llm
        response = chain.invoke({"resume_text": resume_text})
        content = response.content.strip()

        # Try to extract JSON from response
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        return json.loads(content)

    except Exception as e:
        print(f"[Parser] LLM extraction failed: {e}. Using regex fallback.")
        return extract_resume_data_regex(resume_text)


def extract_resume_data_regex(resume_text: str) -> dict:
    """Fallback regex-based resume data extraction."""
    text = resume_text

    # Extract email
    email_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    email = email_match.group() if email_match else None

    # Extract phone
    phone_match = re.search(r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\./0-9]{7,15}', text)
    phone = phone_match.group().strip() if phone_match else None

    # Extract links
    links = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', text)

    # Extract skills (common tech keywords)
    known_skills = [
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "golang",
        "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "matlab",
        "react", "angular", "vue", "next.js", "node.js", "express", "django",
        "flask", "fastapi", "spring", "laravel", ".net", "rails",
        "html", "css", "tailwind", "bootstrap", "sass",
        "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
        "git", "jenkins", "ci/cd", "linux", "nginx",
        "machine learning", "deep learning", "nlp", "computer vision",
        "tensorflow", "pytorch", "pandas", "numpy", "scikit-learn",
        "power bi", "tableau", "figma", "jira", "confluence"
    ]

    text_lower = text.lower()
    found_skills = []
    for skill in known_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found_skills.append(skill.title() if len(skill) > 3 else skill.upper())

    # Categorize skills
    prog_langs = [s for s in found_skills if s.lower() in [
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust", "ruby", "php", "swift", "kotlin"
    ]]
    frameworks_found = [s for s in found_skills if s.lower() in [
        "react", "angular", "vue", "next.js", "node.js", "express", "django", "flask", "fastapi", "spring"
    ]]
    databases_found = [s for s in found_skills if s.lower() in [
        "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch"
    ]]
    cloud_found = [s for s in found_skills if s.lower() in [
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform"
    ]]
    ai_found = [s for s in found_skills if s.lower() in [
        "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch"
    ]]

    # Extract name (first non-empty line that's not an email/phone/link)
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    name = None
    for line in lines[:5]:
        if not email_match or email not in line:
            if not phone_match or phone not in line:
                if not line.startswith("http"):
                    if len(line) < 60 and not any(c.isdigit() for c in line[:3]):
                        name = line
                        break

    # Extract languages
    language_keywords = ["english", "hindi", "tamil", "telugu", "kannada", "malayalam",
                         "bengali", "marathi", "gujarati", "french", "german", "spanish",
                         "japanese", "chinese", "korean", "arabic", "urdu"]
    languages = [l.title() for l in language_keywords if l in text_lower]

    return {
        "full_name": name,
        "email": email,
        "phone": phone,
        "skills": found_skills,
        "technical_skills": [s for s in found_skills if s.lower() not in ["communication", "leadership", "teamwork"]],
        "soft_skills": [],
        "programming_languages": prog_langs,
        "frameworks": frameworks_found,
        "databases": databases_found,
        "cloud_skills": cloud_found,
        "ai_skills": ai_found,
        "education": [],
        "experience": [],
        "projects": [],
        "certifications": [],
        "links": links,
        "languages": languages,
        "summary": None,
    }
