"""
TalentSpark AI — RAG Pipeline Service
Complete Retrieval-Augmented Generation for intelligent job recommendations.
"""

from services.llm_service import get_llm
from services.embeddings import search_similar_jobs
from langchain_core.prompts import ChatPromptTemplate


# --- RAG Prompt Templates ---

JOB_SEARCH_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are TalentSpark AI, an intelligent job search assistant.
Use the following job listings retrieved from the database to answer the user's question.
If no relevant jobs are found, say so clearly and suggest refining the search.
Be helpful, specific, and format your response clearly with job details.

Retrieved Jobs:
{context}"""),
    ("human", "{question}")
])

CAREER_COACH_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are TalentSpark AI Career Coach, a world-class career advisor.
You have access to the user's resume and profile information.
Provide personalized, actionable career advice based on their background.
Be encouraging, specific, and practical.

User Profile:
{user_context}

Conversation History:
{chat_history}"""),
    ("human", "{question}")
])

RESUME_REVIEW_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a senior technical recruiter and resume expert.
Analyze the resume and provide:
1. Overall impression (1-2 sentences)
2. Top 3 strengths
3. Top 3 areas for improvement
4. Specific actionable suggestions
5. Estimated ATS compatibility (High/Medium/Low)
6. Recommended job titles based on the resume

Be constructive, specific, and actionable."""),
    ("human", "{resume_text}")
])

INTERVIEW_PREP_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a technical interview preparation expert.
Generate interview questions based on the role and difficulty level.
For each question, provide:
- The question
- Expected answer (brief)
- Tips for answering

Format as a structured list. Include a mix of technical and behavioral questions."""),
    ("human", """Role: {role}
Difficulty: {difficulty}
Focus Areas: {focus_areas}
Number of Questions: {num_questions}""")
])


def rag_job_search(question: str) -> str:
    """RAG-based job search: embed query → retrieve matching jobs → generate LLM answer."""
    results = search_similar_jobs(question, top_k=5)

    if not results:
        return (
            "No matching jobs found in the database. This could mean:\n"
            "1. Jobs haven't been embedded yet (admin needs to run /rag/embed-jobs)\n"
            "2. No jobs match your specific query\n\n"
            "Try broadening your search terms!"
        )

    # Build context from retrieved jobs
    context_parts = []
    for r in results:
        salary_info = f"₹{r.get('salary_min', 'N/A')}-{r.get('salary_max', 'N/A')} LPA" if r.get('salary_min') else "Not disclosed"
        context_parts.append(
            f"• {r['title']} at {r.get('company_name', 'Unknown Company')}\n"
            f"  Location: {r.get('location', 'Not specified')}\n"
            f"  Salary: {salary_info}\n"
            f"  Skills: {r.get('skills', 'N/A')}\n"
            f"  Match Score: {r['score'] * 100:.0f}%"
        )
    context = "\n\n".join(context_parts)

    try:
        llm = get_llm()
        chain = JOB_SEARCH_PROMPT | llm
        response = chain.invoke({"context": context, "question": question})
        return response.content
    except Exception as e:
        print(f"[RAG Service] LLM failed: {e}. Returning formatted results.")
        return _format_search_results(question, results)


def rag_career_coach(question: str, user_context: str = "", chat_history: str = "") -> str:
    """RAG-based career coaching with user context."""
    try:
        llm = get_llm()
        chain = CAREER_COACH_PROMPT | llm
        response = chain.invoke({
            "user_context": user_context or "No profile information available",
            "chat_history": chat_history or "No previous conversation",
            "question": question,
        })
        return response.content
    except Exception as e:
        print(f"[RAG Career Coach] Error: {e}")
        from services.llm_service import _local_fallback
        return _local_fallback(question)


def rag_resume_review(resume_text: str) -> str:
    """RAG-based resume review and analysis."""
    try:
        llm = get_llm()
        chain = RESUME_REVIEW_PROMPT | llm
        response = chain.invoke({"resume_text": resume_text})
        return response.content
    except Exception as e:
        print(f"[RAG Resume Review] Error: {e}")
        from services.ats import _local_ats_analysis
        analysis = _local_ats_analysis(resume_text)
        return (
            f"### Resume Analysis (Local Engine)\n\n"
            f"**Overall Score**: {analysis['overall_score']}/100\n"
            f"**ATS Score**: {analysis['ats_score']}/100\n\n"
            f"**Strengths**: {', '.join(analysis['strengths'])}\n"
            f"**Weaknesses**: {', '.join(analysis['weaknesses'])}\n\n"
            f"**Suggestions**:\n" + "\n".join(f"• {s}" for s in analysis['suggestions'])
        )


def generate_interview_questions(role: str, difficulty: str = "Medium", focus_areas: str = "", num_questions: int = 10) -> str:
    """Generate role-specific interview questions."""
    try:
        llm = get_llm()
        chain = INTERVIEW_PREP_PROMPT | llm
        response = chain.invoke({
            "role": role,
            "difficulty": difficulty,
            "focus_areas": focus_areas or "General technical and behavioral",
            "num_questions": str(num_questions),
        })
        return response.content
    except Exception as e:
        print(f"[Interview Prep] Error: {e}")
        return _fallback_interview_questions(role, difficulty)


def _format_search_results(question: str, results: list[dict]) -> str:
    """Format search results without LLM."""
    reply = f"### Job Search Results\n\nBased on: *\"{question}\"*\n\n"
    for idx, r in enumerate(results, 1):
        pct = min(100, max(1, int(r['score'] * 100)))
        reply += f"**{idx}. {r['title']}**\n"
        if r.get('company_name'):
            reply += f"🏢 {r['company_name']}\n"
        if r.get('location'):
            reply += f"📍 {r['location']}\n"
        if r.get('salary_min') or r.get('salary_max'):
            reply += f"💰 ₹{r.get('salary_min', 'N/A')}-{r.get('salary_max', 'N/A')} LPA\n"
        if r.get('skills'):
            reply += f"🔧 {r['skills']}\n"
        reply += f"📊 Match: {pct}%\n\n"
    return reply


def _fallback_interview_questions(role: str, difficulty: str) -> str:
    """Fallback interview questions when LLM is offline."""
    return f"""### Interview Questions for {role} ({difficulty})

**Technical Questions:**
1. Explain the difference between REST and GraphQL APIs.
2. How do you handle database migrations in production?
3. What is the difference between SQL and NoSQL databases?
4. Explain the concept of microservices architecture.
5. How do you implement authentication in a web application?

**Behavioral Questions:**
6. Tell me about a challenging project you worked on.
7. How do you prioritize tasks when you have multiple deadlines?
8. Describe a time you had to learn a new technology quickly.
9. How do you handle disagreements with team members?
10. What is your approach to code reviews?

*Note: Questions generated using local engine (LLM offline)*"""
