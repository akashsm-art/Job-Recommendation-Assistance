"""
TalentSpark AI — Embeddings & ChromaDB Service
Vector database operations for semantic search and RAG.
"""

import os
import chromadb
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")

# --- ChromaDB Client (Persistent) ---
_chroma_client = None
_embedding_model = None

# Collection names
JOBS_COLLECTION = "job_descriptions"
RESUMES_COLLECTION = "user_resumes"
COURSES_COLLECTION = "courses"


def get_chroma_client():
    """Get or create persistent ChromaDB client."""
    global _chroma_client
    if _chroma_client is None:
        persist_path = Path(CHROMA_PERSIST_DIR).resolve()
        persist_path.mkdir(parents=True, exist_ok=True)
        _chroma_client = chromadb.PersistentClient(path=str(persist_path))
    return _chroma_client


def get_embedding_model():
    """Get or create the embedding model (FastEmbed)."""
    global _embedding_model
    if _embedding_model is None:
        from fastembed import TextEmbedding
        _embedding_model = TextEmbedding("BAAI/bge-small-en-v1.5")
    return _embedding_model


def embed_text(text: str) -> list[float]:
    """Generate embedding vector for a text string."""
    model = get_embedding_model()
    return next(model.embed([text])).tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for multiple texts."""
    model = get_embedding_model()
    return [emb.tolist() for emb in model.embed(texts)]


# ============================================================
# Jobs Collection Operations
# ============================================================

def get_jobs_collection():
    """Get or create the jobs collection."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=JOBS_COLLECTION,
        metadata={"hnsw:space": "cosine"}
    )


async def embed_all_jobs(db) -> int:
    """Embed all jobs from PostgreSQL into ChromaDB."""
    from sqlalchemy.future import select
    from sqlalchemy.orm import selectinload
    from models.job import Job
    from models.company import Company

    result = await db.execute(
        select(Job).filter(Job.is_active == True).options(selectinload(Job.company))
    )
    jobs = result.scalars().all()

    if not jobs:
        return 0

    collection = get_jobs_collection()

    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for job in jobs:
        # Build rich text for embedding
        skills_text = ", ".join(job.required_skills or [])
        preferred_text = ", ".join(job.preferred_skills or [])
        company_name = job.company.name if job.company else "Unknown"

        text = (
            f"Job Title: {job.title}\n"
            f"Company: {company_name}\n"
            f"Description: {job.description or ''}\n"
            f"Requirements: {job.requirements or ''}\n"
            f"Required Skills: {skills_text}\n"
            f"Preferred Skills: {preferred_text}\n"
            f"Location: {job.location or 'Not specified'}\n"
            f"Job Type: {job.job_type.value if job.job_type else 'full_time'}\n"
            f"Work Mode: {job.work_mode.value if job.work_mode else 'onsite'}\n"
            f"Experience: {job.experience_min or 0}-{job.experience_max or 'N/A'} years\n"
            f"Salary: {job.salary_min or 'N/A'}-{job.salary_max or 'N/A'} {job.currency}"
        )

        vector = embed_text(text)

        ids.append(str(job.id))
        documents.append(text)
        embeddings.append(vector)
        metadatas.append({
            "job_id": job.id,
            "title": job.title,
            "company_name": company_name,
            "company_id": job.company_id,
            "location": job.location or "",
            "salary_min": job.salary_min or 0,
            "salary_max": job.salary_max or 0,
            "experience_min": job.experience_min or 0,
            "experience_max": job.experience_max or 0,
            "job_type": job.job_type.value if job.job_type else "full_time",
            "work_mode": job.work_mode.value if job.work_mode else "onsite",
            "is_remote": job.is_remote,
            "skills": skills_text,
        })

    # Upsert into ChromaDB
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(ids)


def search_similar_jobs(query: str, top_k: int = 10, filters: dict = None) -> list[dict]:
    """Search for similar jobs using semantic similarity."""
    collection = get_jobs_collection()

    query_embedding = embed_text(query)

    # Build ChromaDB where filter
    where_filter = None
    if filters:
        conditions = []
        if filters.get("location"):
            conditions.append({"location": {"$eq": filters["location"]}})
        if filters.get("is_remote"):
            conditions.append({"is_remote": {"$eq": True}})
        if filters.get("job_type"):
            conditions.append({"job_type": {"$eq": filters["job_type"]}})
        if conditions:
            where_filter = {"$and": conditions} if len(conditions) > 1 else conditions[0]

    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )
    except Exception:
        # If filter fails, search without filters
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

    if not results["ids"][0]:
        return []

    jobs = []
    for i, job_id in enumerate(results["ids"][0]):
        distance = results["distances"][0][i] if results["distances"] else 0
        # ChromaDB cosine distance: 0 = identical, 2 = opposite
        # Convert to similarity score: 1 - (distance / 2)
        similarity = max(0, min(1, 1 - (distance / 2)))

        metadata = results["metadatas"][0][i] if results["metadatas"] else {}
        jobs.append({
            "job_id": int(metadata.get("job_id", job_id)),
            "title": metadata.get("title", ""),
            "company_name": metadata.get("company_name", ""),
            "location": metadata.get("location", ""),
            "salary_min": metadata.get("salary_min", 0),
            "salary_max": metadata.get("salary_max", 0),
            "skills": metadata.get("skills", ""),
            "score": round(similarity, 4),
            "document": results["documents"][0][i] if results["documents"] else "",
        })

    return jobs


# ============================================================
# Resume Collection Operations
# ============================================================

def embed_user_resume(user_id: int, resume_text: str, skills: list[str] = None):
    """Embed a user's resume into ChromaDB."""
    client = get_chroma_client()
    collection = client.get_or_create_collection(
        name=RESUMES_COLLECTION,
        metadata={"hnsw:space": "cosine"}
    )

    skills_text = ", ".join(skills or [])
    text = f"Resume:\n{resume_text}\n\nKey Skills: {skills_text}"
    vector = embed_text(text)

    collection.upsert(
        ids=[str(user_id)],
        documents=[text],
        embeddings=[vector],
        metadatas=[{"user_id": user_id, "skills": skills_text}],
    )


def search_candidates(query: str, top_k: int = 10) -> list[dict]:
    """Search for matching candidates using semantic similarity."""
    client = get_chroma_client()
    try:
        collection = client.get_collection(RESUMES_COLLECTION)
    except Exception:
        return []

    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    if not results["ids"][0]:
        return []

    candidates = []
    for i, cand_id in enumerate(results["ids"][0]):
        distance = results["distances"][0][i] if results["distances"] else 0
        similarity = max(0, min(1, 1 - (distance / 2)))
        metadata = results["metadatas"][0][i] if results["metadatas"] else {}
        candidates.append({
            "user_id": int(metadata.get("user_id", cand_id)),
            "skills": metadata.get("skills", ""),
            "score": round(similarity, 4),
        })

    return candidates
