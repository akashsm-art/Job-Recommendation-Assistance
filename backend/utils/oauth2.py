"""
TalentSpark AI — OAuth2 Dependencies
FastAPI dependencies for authentication and role-based access control.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database import get_db
from utils.token import verify_access_token
from models.users import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get the current authenticated user from the JWT token."""
    payload = verify_access_token(token)
    user_id = int(payload["sub"])

    result = await db.execute(
        select(User)
        .filter(User.id == user_id)
        .options(
            selectinload(User.skills),
            selectinload(User.education_records),
            selectinload(User.experience_records),
            selectinload(User.projects),
            selectinload(User.certificates),
        )
    )
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )

    return user


def role_required(allowed_roles: list[str]):
    """
    Dependency factory: restricts access to users with specific roles.

    Usage:
        @router.get("/admin-only")
        async def admin_endpoint(user = Depends(role_required(["admin"]))):
            ...
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.value not in allowed_roles and current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {allowed_roles}"
            )
        return current_user
    return role_checker
