"""
TalentSpark AI — Database Migration Helper
Run this script to create all database tables.

Usage: python migrate.py
"""

import asyncio
from database import engine, Base

# Import all models to ensure they're registered with SQLAlchemy
import models  # noqa: F401


async def create_tables():
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Success: All database tables created successfully!")
    print("Tables created:")
    for table_name in Base.metadata.tables:
        print(f"   - {table_name}")


if __name__ == "__main__":
    asyncio.run(create_tables())
