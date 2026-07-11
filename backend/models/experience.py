"""
TalentSpark AI — Experience Model
Work experience records for candidates.
"""

from database import Base
from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_current = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    technologies = Column(String(1000), nullable=True)  # Comma-separated techs

    # --- Relationship ---
    user = relationship("User", back_populates="experience_records")

    def __repr__(self):
        return f"<Experience(company='{self.company}', role='{self.role}')>"
