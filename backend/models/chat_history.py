"""
TalentSpark AI — ChatHistory Model
Persistent chat history for AI Career Coach sessions.
"""

from database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String(255), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # "human" or "ai"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # --- Relationship ---
    user = relationship("User", back_populates="chat_histories")

    def __repr__(self):
        return f"<ChatHistory(session_id='{self.session_id}', role='{self.role}')>"
