"""
TalentSpark AI — Database Configuration
Async SQLAlchemy engine with PostgreSQL (asyncpg driver).
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:007@localhost:5432/talentspark_db")

# Render cloud deployment — warn if still on localhost fallback
if os.getenv("RENDER") and "localhost" in DATABASE_URL:
    print(
        "WARNING: DATABASE_URL is falling back to localhost on Render. "
        "Ensure DATABASE_URL is set in your Render environment or via render.yaml."
    )

# Convert to async driver URL
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# SSL for cloud-hosted databases
connect_args = {}
if any(host in DATABASE_URL for host in ["supabase.com", "render.com", "neon.tech"]) or "sslmode=require" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?")[0]
    import ssl
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    from uuid import uuid4
    connect_args = {
        "ssl": ssl_context,
        "statement_cache_size": 0,
        "prepared_statement_name_func": lambda: f"__asyncpg_{uuid4().hex}__",
    }

engine = create_async_engine(DATABASE_URL, echo=False, connect_args=connect_args)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()


async def get_db():
    """FastAPI dependency that yields an async database session."""
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
