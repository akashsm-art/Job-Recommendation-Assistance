"""
TalentSpark AI — LLM Service
Central LLM instance management with Groq (LLaMA 3.3 70B) and local fallback.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLAMA_MODEL = "llama-3.3-70b-versatile"

# --- Shared LLM Instance ---
_llm = None


def get_llm() -> ChatGroq:
    """Return the shared LLM instance (lazy initialization)."""
    global _llm
    if _llm is None:
        _llm = ChatGroq(
            model=LLAMA_MODEL,
            groq_api_key=GROQ_API_KEY,
            temperature=0.3,
        )
    return _llm


def invoke_llm(prompt: str, temperature: float = 0.3) -> str:
    """Invoke the LLM with a simple prompt string. Returns content or fallback."""
    try:
        llm = get_llm()
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"[LLM Service] Error: {e}")
        return f"[AI Offline] Unable to process request. Error: {str(e)}"


def invoke_llm_with_messages(messages: list[tuple], temperature: float = 0.3) -> str:
    """Invoke the LLM with structured messages [(role, content), ...]."""
    try:
        from langchain_core.prompts import ChatPromptTemplate
        llm = get_llm()
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | llm
        # Extract variable names from the messages
        variables = {}
        for role, content in messages:
            if role == "placeholder":
                continue
            import re
            found = re.findall(r'\{(\w+)\}', content)
            for var in found:
                if var not in variables:
                    variables[var] = ""
        return chain.invoke(variables).content if not variables else ""
    except Exception as e:
        print(f"[LLM Service] Structured invoke error: {e}")
        return f"[AI Offline] Unable to process request."


def chat_without_memory(query: str) -> str:
    """Simple one-shot chat, no conversation history."""
    try:
        llm = get_llm()
        response = llm.invoke(query)
        return response.content
    except Exception as e:
        print(f"[LLM Service] Chat error: {e}. Falling back.")
        return _local_fallback(query)


def _local_fallback(query: str) -> str:
    """Smart local fallback when LLM is offline."""
    q = query.lower()

    if any(k in q for k in ["hello", "hi", "hey", "greetings"]):
        return (
            "Hello! Welcome to TalentSpark AI! 🚀 I'm your AI Career Assistant. "
            "I can help you find matching jobs, analyze your resume, recommend courses, "
            "and plan your career path. How can I assist you today?"
        )

    if any(k in q for k in ["job", "role", "opportunity", "opening", "career"]):
        return (
            "I can help you find the perfect job! Here's what I can do:\n\n"
            "• 🔍 **Search jobs** by skills, location, or keywords\n"
            "• 📊 **Match analysis** — see how well you fit each role\n"
            "• 📝 **Resume optimization** — improve your chances\n"
            "• 🎯 **Skill gap analysis** — know what to learn\n\n"
            "Try uploading your resume first for personalized recommendations!"
        )

    if any(k in q for k in ["resume", "cv", "ats", "score"]):
        return (
            "Our ATS Resume Analyzer can help! Upload your resume to get:\n\n"
            "• 📊 Overall ATS compatibility score\n"
            "• ✅ Keyword match analysis\n"
            "• 📝 Formatting recommendations\n"
            "• 💡 Improvement suggestions\n"
            "• 🎯 Missing skills identification\n\n"
            "Navigate to your profile to upload your resume!"
        )

    if any(k in q for k in ["course", "learn", "skill", "study", "training"]):
        return (
            "I recommend courses from top platforms based on your skill gaps:\n\n"
            "• Coursera, Udemy, NPTEL, edX\n"
            "• LinkedIn Learning, freeCodeCamp\n"
            "• YouTube tutorials & Roadmap.sh\n\n"
            "Upload your resume and I'll create a personalized learning path!"
        )

    if any(k in q for k in ["interview", "prepare", "practice", "mock"]):
        return (
            "Interview preparation tools include:\n\n"
            "• 📝 Role-specific MCQs\n"
            "• 💻 Coding challenges by difficulty\n"
            "• 🏗️ System design questions\n"
            "• 🗣️ Behavioral & HR questions\n"
            "• 📊 Performance tracking\n\n"
            "Tell me the role you're preparing for!"
        )

    return (
        "I'm your TalentSpark AI Career Assistant! 🚀 Here's how I can help:\n\n"
        "• 🔍 Find matching jobs\n"
        "• 📄 Analyze your resume\n"
        "• 📚 Recommend courses\n"
        "• 🎯 Identify skill gaps\n"
        "• 💼 Prepare for interviews\n"
        "• 🗺️ Plan your career roadmap\n\n"
        "What would you like to do?"
    )
