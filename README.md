# 🚀 TalentSpark AI — AI-Powered Job Recommendation Assistant

An enterprise-grade AI Job Recommendation Platform using **RAG (Retrieval Augmented Generation)**, **Semantic Search**, **AI Embeddings**, **ATS Resume Analysis**, and **LLM Reasoning**.

---

## 🏗️ Tech Stack

### Backend
- **FastAPI** — Async Python web framework
- **PostgreSQL** — Relational database
- **SQLAlchemy** (async) — ORM with asyncpg driver
- **Alembic** — Database migrations
- **JWT + OAuth2** — Authentication
- **LangChain + Groq** — LLM integration (LLaMA 3.3 70B)
- **ChromaDB** — Vector database for semantic search
- **FastEmbed** — Text embeddings (bge-small-en-v1.5)
- **PyMuPDF + python-docx** — Resume parsing

### Frontend (Phase 3)
- React + TypeScript + TailwindCSS + Vite

---

## 📁 Project Structure

```
backend/
├── app/
│   └── main.py              # FastAPI application
├── database.py               # Async SQLAlchemy config
├── migrate.py                 # Table creation helper
├── models/                    # 15 SQLAlchemy models
│   ├── users.py, company.py, job.py
│   ├── application.py, skill.py, education.py
│   ├── experience.py, project.py, certificate.py
│   ├── saved_job.py, notification.py, chat_history.py
│   ├── resume_score.py, course.py, learning_progress.py
│   └── __init__.py
├── schemas/                   # Pydantic validation schemas
│   ├── users.py, company.py, job.py, token.py, application.py
│   ├── resume.py, chat.py, course.py, recommendation.py
│   └── ai_features.py         # [NEW] Phase 2 AI schemas
├── routers/                   # API endpoints
│   ├── users.py               # Auth + Profile (20+ endpoints)
│   ├── company.py             # Company CRUD
│   ├── job.py                 # Jobs + Apply + Save + AI Recommendations
│   ├── rag.py                 # AI/RAG endpoints
│   ├── chat.py                # AI Career Coach
│   └── ai_features.py         # [NEW] Phase 2 Advanced AI features
├── services/                  # Business logic
│   ├── llm_service.py         # Groq LLM integration
│   ├── embeddings.py          # ChromaDB + FastEmbed
│   ├── rag.py                 # RAG pipeline
│   ├── parser.py              # Resume parsing (PDF/DOCX/TXT)
│   ├── ats.py                 # ATS scoring engine
│   ├── recommender.py         # Job recommendation engine
│   ├── similarity.py          # Multi-dimensional matching
│   ├── course_recommender.py  # Course recommendations
│   ├── email.py               # Email notifications
│   ├── salary_predictor.py    # [NEW] AI salary predictor
│   ├── career_roadmap.py      # [NEW] AI career roadmap generator
│   ├── resume_writer.py       # [NEW] AI resume rewriting & cover letters
│   ├── interview_service.py   # [NEW] Enhanced interview prep & evaluations
│   ├── company_fit.py         # [NEW] AI company-candidate fit prediction
│   ├── skill_trends.py        # [NEW] AI skill demand & job market trends
│   ├── resume_builder.py      # [NEW] AI resume HTML builder with templates
│   └── recruiter_ai.py        # [NEW] Candidate ranking, duplicates, fake scan
├── utils/                     # Authentication utilities
│   ├── token.py               # JWT access/refresh/reset tokens
│   ├── security.py            # Password hashing (bcrypt)
│   └── oauth2.py              # Auth dependencies
├── alembic/                   # Database migrations
├── requirements.txt
└── .env
```

---

## 🚀 Quick Start

### 1. Create PostgreSQL Database
```sql
CREATE DATABASE talentspark_db;
```

### 2. Configure Environment
Edit `backend/.env` with your database URL and API keys.

### 3. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Create Tables
```bash
python migrate.py
```

### 5. Run the Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Open API Docs
Visit: http://localhost:8000/docs

---

## 🔑 API Endpoints

| Category | Endpoints | Description |
|----------|-----------|-------------|
| **Auth** | `/auth/register`, `/auth/login`, `/auth/refresh`, `/auth/forgot-password` | Registration, JWT login, refresh tokens |
| **Profile** | `/auth/me`, `/auth/profile`, `/auth/upload-resume` | Profile management, resume upload |
| **Companies** | `/company/` (CRUD) | Company management (recruiter) |
| **Jobs** | `/job/` (CRUD), `/job/search`, `/job/apply` | Job posting, search, apply |
| **AI** | `/rag/search`, `/rag/recommend-jobs`, `/rag/analyze-resume` | RAG search, recommendations, ATS |
| **Chat** | `/chat/`, `/chat/career-coach` | AI career coaching |
| **Skills** | `/job/{id}/skill-gap`, `/rag/recommend-courses` | Skill gap analysis, courses |
| **Advanced AI** | `/ai/predict-salary`, `/ai/career-roadmap`, `/ai/rewrite-resume`, `/ai/generate-cover-letter`, `/ai/interview-prep`, `/ai/evaluate-answer`, `/ai/company-fit`, `/ai/skill-trends`, `/ai/build-resume`, `/ai/rank-candidates`, `/ai/detect-duplicates`, `/ai/resume-authenticity` | All advanced Phase 2 candidate and recruiter AI features |

---

## 👥 User Roles

| Role | Capabilities |
|------|-------------|
| **Candidate** | Browse jobs, apply, upload resume, get AI recommendations, chat with career coach, predict salaries, build roadmaps, practice interviews, check company fit |
| **Recruiter** | Create company, post jobs, view applicants, rank candidates with AI, scan duplicate/fake resumes |
| **Admin** | All recruiter + manage users, verify companies, embed jobs, platform analytics |

//admin@jobcart.com
//jobcart007