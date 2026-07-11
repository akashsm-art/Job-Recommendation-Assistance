"""
TalentSpark AI — Certificate Model
Certifications and credentials for candidates.
"""

from database import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    issuer = Column(String(255), nullable=True)  # "Coursera", "Google", etc.
    issue_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    credential_id = Column(String(255), nullable=True)
    credential_url = Column(String(500), nullable=True)

    # --- Relationship ---
    user = relationship("User", back_populates="certificates")

    def __repr__(self):
        return f"<Certificate(name='{self.name}', issuer='{self.issuer}')>"
