"""
TalentSpark AI — Token Schemas
"""

from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str
