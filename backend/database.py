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

# Render cloud deployment guard
if os.getenv("RENDER") == "true" and "localhost" in DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is missing or misconfigured on Render. "
        "It is currently falling back to localhost, which is not supported in production. "
        "Please add a DATABASE_URL environment variable in your Render Web Service settings."
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
