"""
TalentSpark AI — Chat Schemas
"""

from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    query: str
    response: str


class ChatWithMemoryRequest(BaseModel):
    query: str
    session_id: str


class ChatWithMemoryResponse(BaseModel):
    query: str
    response: str
    session_id: str


class MessageSchema(BaseModel):
    role: str
    content: str


class ChatHistoryResponse(BaseModel):
    session_id: str
    messages: list[MessageSchema]
