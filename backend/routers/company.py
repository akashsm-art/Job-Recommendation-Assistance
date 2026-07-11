"""
TalentSpark AI — Company Router
Company CRUD with recruiter ownership and admin verification.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database import get_db
from models.company import Company
from models.job import Job
from models.users import User
from schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from utils.oauth2 import get_current_user, role_required

router = APIRouter(prefix="/company", tags=["Company"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CompanyResponse)
async def create_company(
    company: CompanyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required(["recruiter", "admin"])),
):
    """Create a new company (recruiter/admin only)."""
    if company.email:
        result = await db.execute(select(Company).filter(Company.email == company.email))
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Company with this email already exists")

    db_company = Company(
        **company.model_dump(),
        owner_id=current_user.id,
    )
    db.add(db_company)
    await db.commit()

    # Reload with relationships
    result = await db.execute(
        select(Company).filter(Company.id == db_company.id)
    )
    return result.scalars().first()


@router.get("/", response_model=list[CompanyResponse])
async def get_all_companies(db: AsyncSession = Depends(get_db)):
    """Get all active companies (public)."""
    result = await db.execute(
        select(Company).filter(Company.is_active == True).order_by(Company.created_at.desc())
    )
    return result.scalars().all()


@router.get("/my-companies", response_model=list[CompanyResponse])
async def get_my_companies(
    current_user: User = Depends(role_required(["recruiter", "admin"])),
    db: AsyncSession = Depends(get_db),
):
    """Get companies owned by the current recruiter."""
    result = await db.execute(
        select(Company).filter(Company.owner_id == current_user.id)
    )
    return result.scalars().all()


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: int, db: AsyncSession = Depends(get_db)):
    """Get a company by ID (public)."""
    result = await db.execute(
        select(Company).filter(Company.id == company_id)
    )
    company = result.scalars().first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    company_update: CompanyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required(["recruiter", "admin"])),
):
    """Update a company (owner or admin only)."""
    result = await db.execute(select(Company).filter(Company.id == company_id))
    company = result.scalars().first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Check ownership (unless admin)
    if current_user.role.value != "admin" and company.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own company")

    # Check email uniqueness
    update_data = company_update.model_dump(exclude_unset=True)
    if "email" in update_data and update_data["email"] != company.email:
        email_check = await db.execute(select(Company).filter(Company.email == update_data["email"]))
        if email_check.scalars().first():
            raise HTTPException(status_code=400, detail="Company with this email already exists")

    for key, value in update_data.items():
        setattr(company, key, value)

    await db.commit()

    result = await db.execute(select(Company).filter(Company.id == company_id))
    return result.scalars().first()


@router.delete("/{company_id}")
async def delete_company(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required(["recruiter", "admin"])),
):
    """Delete a company (owner or admin only)."""
    result = await db.execute(select(Company).filter(Company.id == company_id))
    company = result.scalars().first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    if current_user.role.value != "admin" and company.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own company")

    await db.delete(company)
    await db.commit()
    return {"detail": "Company deleted successfully"}


@router.put("/{company_id}/verify")
async def verify_company(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(role_required(["admin"])),
):
    """Admin: Verify a company."""
    result = await db.execute(select(Company).filter(Company.id == company_id))
    company = result.scalars().first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    company.is_verified = True
    await db.commit()
    return {"detail": f"Company '{company.name}' verified successfully"}
