"""
TalentSpark AI — ResumeScore Model
ATS analysis scores and detailed breakdown.
"""

from database import Base
from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime


class ResumeScore(Base):
    __tablename__ = "resume_scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # --- Scores (0-100) ---
    ats_score = Column(Float, nullable=True)
    formatting_score = Column(Float, nullable=True)
    keyword_score = Column(Float, nullable=True)
    grammar_score = Column(Float, nullable=True)
    projects_score = Column(Float, nullable=True)
    experience_score = Column(Float, nullable=True)
    skills_score = Column(Float, nullable=True)
    education_score = Column(Float, nullable=True)
    overall_score = Column(Float, nullable=True)

    # --- Detailed Analysis ---
    suggestions = Column(JSON, nullable=True)     # List of improvement suggestions
    missing_skills = Column(JSON, nullable=True)   # Skills to add
    missing_keywords = Column(JSON, nullable=True) # Keywords to include
    strengths = Column(JSON, nullable=True)        # Resume strengths
    weaknesses = Column(JSON, nullable=True)       # Resume weaknesses
    heatmap_data = Column(JSON, nullable=True)     # Section-wise score distribution

    # --- Raw Analysis ---
    full_analysis = Column(Text, nullable=True)    # Complete LLM analysis text

    created_at = Column(DateTime, default=datetime.utcnow)

    # --- Relationship ---
    user = relationship("User", back_populates="resume_scores")

    def __repr__(self):
        return f"<ResumeScore(user_id={self.user_id}, overall={self.overall_score})>"
