"""
TalentSpark AI — Main Application
FastAPI entry point with CORS, all routers, and startup events.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import PlainTextResponse
from pathlib import Path
import os

from routers import users, company, job, rag, chat, ai_features
from database import Base, engine

# Ensure all models are imported for SQLAlchemy discovery
import models  # noqa: F401

# --- Application ---
app = FastAPI(
    title="JOBCART",
    description=(
        "🚀 AI-Powered Job Recommendation Assistant using RAG, "
        "Semantic Search, AI Embeddings, Resume Parsing, Skill Matching, and LLM Reasoning."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        os.getenv("FRONTEND_URL", "http://localhost:5173"),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Static Files (Uploads) ---
upload_dir = Path(os.getenv("UPLOAD_DIR", "./uploads"))
upload_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")

# --- Startup Event ---
@app.on_event("startup")
async def startup_event():
    """Create database tables on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created/verified")
    print("jobcart is on live !!!!")


# --- Include Routers ---
app.include_router(users.router)
app.include_router(company.router)
app.include_router(job.router)
app.include_router(rag.router)
app.include_router(chat.router)
app.include_router(ai_features.router)


# --- Root Endpoints ---
@app.get("/", tags=["Health"], response_class=PlainTextResponse)
def read_root():
    return "jobcart is on live !!!!"


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "JOBCART"}
