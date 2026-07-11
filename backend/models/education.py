"""
TalentSpark AI — Education Model
Academic records for candidates.
"""

from database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    degree = Column(String(255), nullable=False)  # "B.Tech", "M.Sc", "MBA", etc.
    field_of_study = Column(String(255), nullable=True)  # "Computer Science", etc.
    institution = Column(String(255), nullable=False)
    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)
    cgpa = Column(Float, nullable=True)
    grade = Column(String(10), nullable=True)  # "A+", "First Class", etc.
    description = Column(String(1000), nullable=True)

    # --- Relationship ---
    user = relationship("User", back_populates="education_records")

    def __repr__(self):
        return f"<Education(degree='{self.degree}', institution='{self.institution}')>"
