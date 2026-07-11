"""
TalentSpark AI — Chat Router
AI Career Coach with session-based memory.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db
from models.users import User
from models.chat_history import ChatHistory
from schemas.chat import (
    ChatRequest, ChatResponse,
    ChatWithMemoryRequest, ChatWithMemoryResponse,
    ChatHistoryResponse, MessageSchema,
)
from utils.oauth2 import get_current_user

router = APIRouter(prefix="/chat", tags=["AI Chat"])


@router.post("/", response_model=ChatResponse)
def simple_chat(request: ChatRequest):
    """Simple one-shot chat — no memory, no session."""
    try:
        from services.llm_service import chat_without_memory
        response = chat_without_memory(request.query)
        return ChatResponse(query=request.query, response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/career-coach", response_model=ChatWithMemoryResponse)
async def career_coach_chat(
    request: ChatWithMemoryRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """AI Career Coach with context-aware responses and session memory."""
    try:
        # Build user context from profile
        user_context_parts = []
        if current_user.full_name:
            user_context_parts.append(f"Name: {current_user.full_name}")
        if current_user.technical_skills:
            user_context_parts.append(f"Technical Skills: {', '.join(current_user.technical_skills[:10])}")
        if current_user.experience_years:
            user_context_parts.append(f"Experience: {current_user.experience_years} years")
        if current_user.preferred_role:
            user_context_parts.append(f"Target Role: {current_user.preferred_role}")
        if current_user.highest_qualification:
            user_context_parts.append(f"Education: {current_user.highest_qualification}")
        if current_user.career_objective:
            user_context_parts.append(f"Career Goal: {current_user.career_objective}")

        user_context = "\n".join(user_context_parts) if user_context_parts else "No profile information"

        # Get recent chat history for context
        history_result = await db.execute(
            select(ChatHistory)
            .filter(
                ChatHistory.user_id == current_user.id,
                ChatHistory.session_id == request.session_id,
            )
            .order_by(ChatHistory.created_at.desc())
            .limit(10)
        )
        history_records = history_result.scalars().all()
        history_records.reverse()

        chat_history = "\n".join([
            f"{'User' if h.role == 'human' else 'AI'}: {h.content}"
            for h in history_records
        ])

        # Generate response using RAG career coach
        from services.rag import rag_career_coach
        response = rag_career_coach(request.query, user_context, chat_history)

        # Save to history
        user_msg = ChatHistory(
            user_id=current_user.id,
            session_id=request.session_id,
            role="human",
            content=request.query,
        )
        ai_msg = ChatHistory(
            user_id=current_user.id,
            session_id=request.session_id,
            role="ai",
            content=response,
        )
        db.add(user_msg)
        db.add(ai_msg)
        await db.commit()

        return ChatWithMemoryResponse(
            query=request.query,
            response=response,
            session_id=request.session_id,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get chat history for a session."""
    result = await db.execute(
        select(ChatHistory)
        .filter(
            ChatHistory.user_id == current_user.id,
            ChatHistory.session_id == session_id,
        )
        .order_by(ChatHistory.created_at.asc())
    )
    records = result.scalars().all()
    messages = [MessageSchema(role=r.role, content=r.content) for r in records]
    return ChatHistoryResponse(session_id=session_id, messages=messages)


@router.delete("/history/{session_id}")
async def delete_chat_history(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Clear chat history for a session."""
    result = await db.execute(
        select(ChatHistory)
        .filter(
            ChatHistory.user_id == current_user.id,
            ChatHistory.session_id == session_id,
        )
    )
    records = result.scalars().all()

    if not records:
        raise HTTPException(status_code=404, detail="Session not found")

    for record in records:
        await db.delete(record)
    await db.commit()

    return {"message": f"Chat history for session '{session_id}' cleared."}


@router.get("/sessions")
async def get_chat_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all chat sessions for the current user."""
    from sqlalchemy import func

    result = await db.execute(
        select(
            ChatHistory.session_id,
            func.count(ChatHistory.id).label("message_count"),
            func.max(ChatHistory.created_at).label("last_message"),
        )
        .filter(ChatHistory.user_id == current_user.id)
        .group_by(ChatHistory.session_id)
        .order_by(func.max(ChatHistory.created_at).desc())
    )

    sessions = []
    for row in result.all():
        sessions.append({
            "session_id": row.session_id,
            "message_count": row.message_count,
            "last_message": str(row.last_message),
        })

    return {"sessions": sessions}
