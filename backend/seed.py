"""
TalentSpark AI — Database Seeding Script
Creates initial companies, jobs, and courses for testing.
"""

import asyncio
from database import engine, SessionLocal
from models.company import Company
from models.job import Job
from models.course import Course
from models.users import User, UserRole
from utils.security import hash_password
from sqlalchemy.future import select


async def seed():
    async with engine.begin() as conn:
        # Tables are created on startup, but let's make sure
        pass

    db = SessionLocal()
    try:
        # 1. Create default admin and recruiter users
        admin_check = await db.execute(select(User).filter(User.email == "admin@talentspark.ai"))
        admin = admin_check.scalars().first()
        if not admin:
            admin = User(
                full_name="Platform Admin",
                email="admin@talentspark.ai",
                hashed_password=hash_password("admin123"),
                role=UserRole.ADMIN,
                is_verified=True,
                is_active=True,
            )
            db.add(admin)

        recruiter_check = await db.execute(select(User).filter(User.email == "recruiter@acme.com"))
        recruiter = recruiter_check.scalars().first()
        if not recruiter:
            recruiter = User(
                full_name="Sarah Jenkins",
                email="recruiter@acme.com",
                hashed_password=hash_password("recruiter123"),
                role=UserRole.RECRUITER,
                is_verified=True,
                is_active=True,
            )
            db.add(recruiter)

        candidate_check = await db.execute(select(User).filter(User.email == "candidate@talentspark.ai"))
        candidate = candidate_check.scalars().first()
        if not candidate:
            candidate = User(
                full_name="John Doe",
                email="candidate@talentspark.ai",
                hashed_password=hash_password("candidate123"),
                role=UserRole.CANDIDATE,
                is_verified=True,
                is_active=True,
                technical_skills=["Python", "React", "SQL"],
                experience_years=3.0,
                preferred_role="Full Stack Developer",
                preferred_location="Bangalore",
            )
            db.add(candidate)

        await db.commit()
        await db.refresh(recruiter)

        # 2. Create Companies
        company_check = await db.execute(select(Company).filter(Company.name == "Acme Corporation"))
        acme = company_check.scalars().first()
        if not acme:
            acme = Company(
                name="Acme Corporation",
                email="contact@acme.com",
                phone="+91 80 4910 2000",
                website="https://acme.corp",
                description="Acme Corporation is a leading provider of SaaS solutions and enterprise software.",
                industry="Software / SaaS",
                company_size="500-1000 employees",
                founded_year=2012,
                tech_stack=["React", "TypeScript", "FastAPI", "PostgreSQL", "Docker", "AWS"],
                headquarters="Bangalore",
                locations=["Bangalore", "Hyderabad", "Remote"],
                owner_id=recruiter.id,
                is_verified=True,
                is_active=True,
                culture="Innovative, fast-paced, employee-centric.",
                benefits=["Health Insurance", "Remote Work Allowance", "Gym Membership", "Learning Budgets"],
            )
            db.add(acme)

        techcorp_check = await db.execute(select(Company).filter(Company.name == "TechCorp Systems"))
        techcorp = techcorp_check.scalars().first()
        if not techcorp:
            techcorp = Company(
                name="TechCorp Systems",
                email="careers@techcorp.com",
                phone="+91 40 5912 3000",
                website="https://techcorp.systems",
                description="TechCorp specializes in large-scale backend infrastructure and AI enablement platforms.",
                industry="Artificial Intelligence / DevOps",
                company_size="100-500 employees",
                founded_year=2018,
                tech_stack=["Python", "Go", "Kubernetes", "ChromaDB", "AWS", "PyTorch"],
                headquarters="Hyderabad",
                locations=["Hyderabad", "Pune", "Remote"],
                owner_id=recruiter.id,
                is_verified=True,
                is_active=True,
                culture="Research-oriented, collaborative, flexible hours.",
                benefits=["Flexible Hours", "Equity Options", "Free Meals", "Conference Allowances"],
            )
            db.add(techcorp)

        await db.commit()
        await db.refresh(acme)
        await db.refresh(techcorp)

        # 3. Create Jobs
        job1_check = await db.execute(select(Job).filter(Job.title == "Full Stack Software Engineer"))
        if not job1_check.scalars().first():
            job1 = Job(
                title="Full Stack Software Engineer",
                description="We are looking for a skilled Full Stack Engineer to design and implement client-facing SaaS dashboards.",
                requirements="Minimum 2 years experience with React and Python APIs. Knowledge of PostgreSQL is required.",
                responsibilities="Develop frontend pages, design REST APIs, optimize database queries, write unit tests.",
                salary_min=10.0,
                salary_max=18.0,
                currency="INR",
                experience_min=2.0,
                experience_max=5.0,
                location="Bangalore",
                is_remote=False,
                required_skills=["React", "FastAPI", "PostgreSQL", "JavaScript"],
                preferred_skills=["TypeScript", "Docker"],
                min_qualification="B.Tech Computer Science",
                company_id=acme.id,
                is_active=True,
                tags=["React", "Python", "Full-Stack"],
                benefits=["Flexible hours", "Health insurance"],
            )
            db.add(job1)

        job2_check = await db.execute(select(Job).filter(Job.title == "AI & Python SDE"))
        if not job2_check.scalars().first():
            job2 = Job(
                title="AI & Python SDE",
                description="Join our AI Core team to build RAG pipelines, manage embeddings, and deploy LLM agents.",
                requirements="3+ years of experience with Python, FastAPI, and Vector Databases (Chroma/Qdrant).",
                responsibilities="Implement search pipelines, design neural search filters, deploy model APIs.",
                salary_min=15.0,
                salary_max=28.0,
                currency="INR",
                experience_min=3.0,
                experience_max=7.0,
                location="Remote",
                is_remote=True,
                required_skills=["Python", "FastAPI", "ChromaDB", "Machine Learning"],
                preferred_skills=["PyTorch", "Kubernetes"],
                min_qualification="B.Tech / M.Tech",
                company_id=techcorp.id,
                is_active=True,
                tags=["AI", "Python", "RAG"],
                benefits=["Remote work", "Equity options"],
            )
            db.add(job2)

        # 4. Create Courses
        courses_data = [
            {"title": "Python for Everybody", "provider": "Coursera", "url": "https://www.coursera.org/specializations/python", "rating": 4.8, "duration": "8 months", "difficulty": "Beginner", "skill": "Python", "is_free": True},
            {"title": "React - The Complete Guide", "provider": "Udemy", "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/", "rating": 4.7, "duration": "68 hours", "difficulty": "Intermediate", "skill": "React", "is_free": False},
            {"title": "Docker Mastery", "provider": "Udemy", "url": "https://www.udemy.com/course/docker-mastery/", "rating": 4.7, "duration": "20 hours", "difficulty": "Intermediate", "skill": "Docker", "is_free": False},
            {"title": "Machine Learning by Andrew Ng", "provider": "Coursera", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "rating": 4.9, "duration": "3 months", "difficulty": "Intermediate", "skill": "Machine Learning", "is_free": True},
        ]

        for c_data in courses_data:
            c_check = await db.execute(select(Course).filter(Course.title == c_data["title"]))
            if not c_check.scalars().first():
                db_course = Course(**c_data)
                db.add(db_course)

        await db.commit()
        print("✅ Database successfully seeded with test companies, jobs, courses, and roles!")

    except Exception as e:
        await db.rollback()
        print(f"❌ Seeding failed: {e}")
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(seed())
