"""
TalentSpark AI — Project Model
Project portfolio for candidates.
"""

from database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    tech_stack = Column(JSON, nullable=True)  # ["Python", "React", ...]
    url = Column(String(500), nullable=True)  # Live demo URL
    github_url = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)
    start_date = Column(String(20), nullable=True)
    end_date = Column(String(20), nullable=True)

    # --- Relationship ---
    user = relationship("User", back_populates="projects")

    def __repr__(self):
        return f"<Project(title='{self.title}')>"
