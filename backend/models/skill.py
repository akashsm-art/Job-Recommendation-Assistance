"""
TalentSpark AI — Skill Model
User skills with categories and proficiency levels.
"""

from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
import enum


class SkillCategory(str, enum.Enum):
    TECHNICAL = "technical"
    SOFT = "soft"
    PROGRAMMING_LANGUAGE = "programming_language"
    FRAMEWORK = "framework"
    DATABASE = "database"
    CLOUD = "cloud"
    AI_ML = "ai_ml"
    DEVOPS = "devops"
    TOOL = "tool"
    OTHER = "other"


class ProficiencyLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False, index=True)
    category = Column(SAEnum(SkillCategory), default=SkillCategory.TECHNICAL)
    proficiency = Column(SAEnum(ProficiencyLevel), default=ProficiencyLevel.INTERMEDIATE)

    # --- Relationship ---
    user = relationship("User", back_populates="skills")

    def __repr__(self):
        return f"<Skill(name='{self.name}', category='{self.category}')>"
