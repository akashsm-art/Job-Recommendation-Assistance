"""
TalentSpark AI — Model Registry
Import all models here so SQLAlchemy discovers them for table creation and Alembic migrations.
"""

from models.users import User, UserRole, WorkMode, Gender
from models.company import Company
from models.job import Job, JobType, WorkModeJob
from models.application import Application, ApplicationStatus
from models.skill import Skill, SkillCategory, ProficiencyLevel
from models.education import Education
from models.experience import Experience
from models.project import Project
from models.certificate import Certificate
from models.saved_job import SavedJob
from models.notification import Notification, NotificationType
from models.chat_history import ChatHistory
from models.resume_score import ResumeScore
from models.course import Course
from models.learning_progress import LearningProgress, LearningStatus

__all__ = [
    "User", "UserRole", "WorkMode", "Gender",
    "Company",
    "Job", "JobType", "WorkModeJob",
    "Application", "ApplicationStatus",
    "Skill", "SkillCategory", "ProficiencyLevel",
    "Education",
    "Experience",
    "Project",
    "Certificate",
    "SavedJob",
    "Notification", "NotificationType",
    "ChatHistory",
    "ResumeScore",
    "Course",
    "LearningProgress", "LearningStatus",
]
