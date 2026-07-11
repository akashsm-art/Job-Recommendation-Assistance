"""
TalentSpark AI — Course Model
Course catalog for skill development recommendations.
"""

from database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from sqlalchemy.orm import relationship


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    provider = Column(String(255), nullable=False)  # "Coursera", "Udemy", "NPTEL", etc.
    url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    instructor = Column(String(255), nullable=True)
    rating = Column(Float, nullable=True)
    duration = Column(String(100), nullable=True)  # "4 weeks", "10 hours", etc.
    difficulty = Column(String(50), nullable=True)  # "Beginner", "Intermediate", "Advanced"
    skill = Column(String(255), nullable=True, index=True)  # Primary skill this course teaches
    category = Column(String(255), nullable=True)  # "Programming", "AI/ML", "Cloud", etc.
    is_free = Column(Boolean, default=False)
    has_certificate = Column(Boolean, default=True)
    price = Column(String(50), nullable=True)
    image_url = Column(String(500), nullable=True)
    estimated_completion = Column(String(100), nullable=True)

    # --- Relationships ---
    learning_progress = relationship("LearningProgress", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Course(title='{self.title}', provider='{self.provider}')>"
