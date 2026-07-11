"""
TalentSpark AI — Enhanced Interview Service
Generate comprehensive interview preparation materials including MCQs,
coding questions, system design, HR, and behavioral questions.
"""

import json
from typing import Optional


# Pre-built question banks by category
QUESTION_BANKS = {
    "python": {
        "mcq": [
            {"q": "What is the output of `print(type([]) is list)`?", "options": ["True", "False", "Error", "None"], "answer": "True", "explanation": "type([]) returns <class 'list'>, which is indeed list."},
            {"q": "Which of the following is immutable in Python?", "options": ["List", "Dictionary", "Tuple", "Set"], "answer": "Tuple", "explanation": "Tuples are immutable sequences in Python."},
            {"q": "What does `*args` in a function definition allow?", "options": ["Keyword arguments", "Variable positional arguments", "Default arguments", "No arguments"], "answer": "Variable positional arguments", "explanation": "*args collects extra positional arguments as a tuple."},
            {"q": "What is a Python decorator?", "options": ["A class method", "A function that modifies another function", "A type of loop", "An import statement"], "answer": "A function that modifies another function", "explanation": "Decorators wrap functions to extend their behavior."},
            {"q": "What is the time complexity of `dict.get(key)`?", "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"], "answer": "O(1)", "explanation": "Dictionary lookups use hash tables, providing O(1) average time."},
        ],
        "coding": [
            {"title": "Two Sum", "difficulty": "Easy", "description": "Given an array of integers and a target, return indices of two numbers that add up to the target.", "hint": "Use a hash map for O(n) solution."},
            {"title": "Reverse Linked List", "difficulty": "Easy", "description": "Reverse a singly linked list iteratively.", "hint": "Use three pointers: prev, curr, next."},
            {"title": "LRU Cache", "difficulty": "Medium", "description": "Design and implement an LRU cache with get and put operations in O(1).", "hint": "Use OrderedDict or doubly-linked list + hash map."},
        ],
    },
    "react": {
        "mcq": [
            {"q": "What is the virtual DOM in React?", "options": ["A real DOM copy", "A lightweight JavaScript representation of the DOM", "A browser API", "A CSS framework"], "answer": "A lightweight JavaScript representation of the DOM", "explanation": "React uses a virtual DOM to efficiently update the real DOM."},
            {"q": "What hook replaces componentDidMount?", "options": ["useState", "useEffect", "useContext", "useReducer"], "answer": "useEffect", "explanation": "useEffect with empty dependency array runs once after mount."},
            {"q": "What is JSX?", "options": ["JavaScript XML", "Java Syntax Extension", "JSON Schema", "JavaScript XHR"], "answer": "JavaScript XML", "explanation": "JSX is a syntax extension that looks like HTML but compiles to JavaScript."},
        ],
        "coding": [
            {"title": "Counter Component", "difficulty": "Easy", "description": "Build a counter component with increment, decrement, and reset buttons using useState."},
            {"title": "Todo App with Context", "difficulty": "Medium", "description": "Create a todo app using React Context for state management with add, toggle, delete."},
        ],
    },
    "system_design": [
        {"title": "Design a URL Shortener", "difficulty": "Medium", "topics": ["Hashing", "Database", "API Design", "Caching"], "key_points": ["Base62 encoding", "Read-heavy workload", "Cache with Redis", "Analytics tracking"]},
        {"title": "Design a Chat Application", "difficulty": "Hard", "topics": ["WebSockets", "Message Queue", "Database Sharding", "Presence System"], "key_points": ["Real-time messaging", "Message ordering", "Read receipts", "Group chats"]},
        {"title": "Design a Job Board (like TalentSpark)", "difficulty": "Medium", "topics": ["Search", "Recommendations", "Notifications", "Scalability"], "key_points": ["Full-text search", "Recommendation engine", "Email notifications", "CDN for static assets"]},
        {"title": "Design a Recommendation System", "difficulty": "Hard", "topics": ["ML Models", "Collaborative Filtering", "Content-Based", "A/B Testing"], "key_points": ["Feature engineering", "Real-time vs batch", "Cold start problem", "Evaluation metrics"]},
    ],
    "hr": [
        {"q": "Tell me about yourself.", "tips": "Follow the Present-Past-Future formula. Start with current role, then relevant experience, then career goals.", "category": "Introduction"},
        {"q": "Why do you want to work here?", "tips": "Research the company. Mention specific projects, culture, or values that align with your goals.", "category": "Motivation"},
        {"q": "What are your strengths and weaknesses?", "tips": "Be genuine. Frame weaknesses as areas of growth with specific improvement actions.", "category": "Self-awareness"},
        {"q": "Where do you see yourself in 5 years?", "tips": "Show ambition but be realistic. Align with the company's growth trajectory.", "category": "Vision"},
        {"q": "Why are you leaving your current job?", "tips": "Stay positive. Focus on growth opportunities rather than problems with current employer.", "category": "Career Change"},
        {"q": "Tell me about a time you handled conflict.", "tips": "Use the STAR method (Situation, Task, Action, Result). Show maturity and resolution skills.", "category": "Behavioral"},
        {"q": "How do you handle pressure and deadlines?", "tips": "Give specific examples. Mention prioritization techniques and stress management.", "category": "Work Style"},
        {"q": "What salary are you expecting?", "tips": "Research market rates. Give a range based on your experience and the role.", "category": "Compensation"},
    ],
}


def generate_interview_prep(
    role: str,
    difficulty: str = "Medium",
    categories: list[str] = None,
    num_questions: int = 10,
    company: str = None,
    user_skills: list[str] = None,
) -> dict:
    """Generate comprehensive interview preparation materials."""

    if categories is None:
        categories = ["mcq", "coding", "system_design", "hr", "behavioral"]

    result = {
        "role": role,
        "difficulty": difficulty,
        "company": company,
        "sections": {},
        "tips": _get_interview_tips(role),
    }

    # MCQs
    if "mcq" in categories:
        result["sections"]["mcq"] = _get_mcq_questions(role, user_skills, difficulty, num_questions)

    # Coding
    if "coding" in categories:
        result["sections"]["coding"] = _get_coding_questions(role, difficulty)

    # System Design
    if "system_design" in categories:
        result["sections"]["system_design"] = QUESTION_BANKS.get("system_design", [])

    # HR & Behavioral
    if "hr" in categories or "behavioral" in categories:
        result["sections"]["hr_behavioral"] = QUESTION_BANKS.get("hr", [])

    # Company-specific questions
    if company:
        result["sections"]["company_specific"] = _generate_company_questions(company, role)

    return result


def generate_mock_interview(role: str, difficulty: str = "Medium", num_rounds: int = 3) -> dict:
    """Generate a mock interview structure with multiple rounds."""
    rounds = []

    if num_rounds >= 1:
        rounds.append({
            "round": 1,
            "title": "📋 Technical Screening",
            "duration": "30 minutes",
            "type": "MCQ + Short Answer",
            "questions": _get_mcq_questions(role, None, difficulty, 5),
            "scoring": {"pass_threshold": 60, "total_marks": 100},
        })

    if num_rounds >= 2:
        rounds.append({
            "round": 2,
            "title": "💻 Coding Round",
            "duration": "60 minutes",
            "type": "Coding Problems",
            "questions": _get_coding_questions(role, difficulty),
            "scoring": {"pass_threshold": 70, "criteria": ["Correctness", "Optimization", "Code Quality"]},
        })

    if num_rounds >= 3:
        rounds.append({
            "round": 3,
            "title": "🏗️ System Design / HR",
            "duration": "45 minutes",
            "type": "System Design + Behavioral",
            "questions": QUESTION_BANKS.get("system_design", [])[:2] + QUESTION_BANKS.get("hr", [])[:3],
            "scoring": {"pass_threshold": 60, "criteria": ["Design Thinking", "Communication", "Problem Solving"]},
        })

    return {
        "role": role,
        "difficulty": difficulty,
        "total_rounds": len(rounds),
        "estimated_duration": f"{sum(30 * (i+1) for i in range(len(rounds)))} minutes",
        "rounds": rounds,
    }


def evaluate_interview_response(question: str, answer: str, role: str) -> dict:
    """Use LLM to evaluate an interview response."""
    from services.llm_service import get_llm
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a senior technical interviewer evaluating a candidate's response.
Evaluate the answer and return a valid JSON object:
{{
    "score": 75,
    "max_score": 100,
    "feedback": "Detailed constructive feedback",
    "strengths": ["What was good about the answer"],
    "improvements": ["What could be better"],
    "ideal_answer_outline": "Brief outline of an ideal answer",
    "communication_score": 70,
    "technical_score": 80,
    "confidence_score": 65
}}
Be fair but constructive. Return ONLY valid JSON."""),
        ("human", """Role: {role}
Question: {question}
Candidate's Answer: {answer}""")
    ])

    try:
        llm = get_llm()
        chain = prompt | llm
        response = chain.invoke({"role": role, "question": question, "answer": answer})
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        return {
            "score": 60, "max_score": 100,
            "feedback": "Answer received. LLM evaluation unavailable.",
            "strengths": ["Answer was provided"],
            "improvements": ["Add more specific examples", "Include technical details"],
            "communication_score": 60, "technical_score": 60, "confidence_score": 60,
        }


def _get_mcq_questions(role: str, skills: list, difficulty: str, count: int) -> list:
    """Get MCQ questions relevant to the role and skills."""
    questions = []
    # Gather from question banks
    for skill_key in ["python", "react"]:
        bank = QUESTION_BANKS.get(skill_key, {})
        if "mcq" in bank:
            questions.extend(bank["mcq"])

    # If we have enough, return subset
    if questions:
        return questions[:count]

    # Otherwise use LLM
    return _generate_mcq_with_llm(role, difficulty, count)


def _get_coding_questions(role: str, difficulty: str) -> list:
    """Get coding questions for the role."""
    questions = []
    for skill_key in ["python", "react"]:
        bank = QUESTION_BANKS.get(skill_key, {})
        if "coding" in bank:
            questions.extend(bank["coding"])
    return questions[:5]


def _generate_company_questions(company: str, role: str) -> list:
    """Generate company-specific interview questions."""
    return [
        {"q": f"Why do you want to join {company}?", "tips": f"Research {company}'s recent news, products, and culture."},
        {"q": f"How does your experience align with {company}'s mission?", "tips": "Connect your skills to their specific needs."},
        {"q": f"What challenges do you think {company} faces as a {role}?", "tips": "Show industry awareness and strategic thinking."},
    ]


def _generate_mcq_with_llm(role: str, difficulty: str, count: int) -> list:
    """Generate MCQs using LLM."""
    from services.llm_service import get_llm
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages([
        ("system", """Generate {count} multiple-choice questions for a {role} interview at {difficulty} difficulty.
Return a JSON array of objects with: q, options (4 items), answer, explanation.
Return ONLY valid JSON array."""),
        ("human", "Generate the questions now.")
    ])

    try:
        llm = get_llm()
        chain = prompt | llm
        response = chain.invoke({"role": role, "difficulty": difficulty, "count": str(count)})
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except:
        return [{"q": "What is your approach to problem solving?", "options": ["Brute force", "Divide and conquer", "Depends on the problem", "Random"], "answer": "Depends on the problem", "explanation": "Good engineers analyze the problem first."}]


def _get_interview_tips(role: str) -> list:
    """Get general interview tips."""
    return [
        "🔍 Research the company thoroughly before the interview",
        "💡 Use the STAR method for behavioral questions (Situation, Task, Action, Result)",
        "🗣️ Think out loud during coding/design rounds — process matters more than perfect answers",
        "❓ Prepare 3-5 thoughtful questions to ask the interviewer",
        "⏱️ Practice time management — allocate time for each problem",
        "📝 Review your resume — be ready to discuss every project and experience",
        "🧘 Stay calm and take a moment to think before answering",
        "🔄 If stuck, describe your thought process and ask clarifying questions",
    ]
