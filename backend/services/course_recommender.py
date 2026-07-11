"""
TalentSpark AI — Course Recommender Service
Recommend courses based on skill gaps and learning goals.
"""

# Pre-built course database for common skills
COURSE_DATABASE = {
    "python": [
        {"title": "Python for Everybody", "provider": "Coursera", "url": "https://www.coursera.org/specializations/python", "rating": 4.8, "duration": "8 months", "difficulty": "Beginner", "is_free": True, "has_certificate": True, "price": "Free (Audit)", "estimated_completion": "2-3 months"},
        {"title": "Complete Python Bootcamp", "provider": "Udemy", "url": "https://www.udemy.com/course/complete-python-bootcamp/", "rating": 4.6, "duration": "22 hours", "difficulty": "Beginner", "is_free": False, "has_certificate": True, "price": "₹449", "estimated_completion": "3 weeks"},
        {"title": "Programming in Python", "provider": "NPTEL", "url": "https://nptel.ac.in/courses/106106182", "rating": 4.5, "duration": "12 weeks", "difficulty": "Intermediate", "is_free": True, "has_certificate": True, "price": "Free", "estimated_completion": "3 months"},
    ],
    "javascript": [
        {"title": "JavaScript: Understanding the Weird Parts", "provider": "Udemy", "url": "https://www.udemy.com/course/understand-javascript/", "rating": 4.7, "duration": "12 hours", "difficulty": "Intermediate", "is_free": False, "has_certificate": True, "price": "₹449", "estimated_completion": "2 weeks"},
        {"title": "The Complete JavaScript Course", "provider": "Udemy", "url": "https://www.udemy.com/course/the-complete-javascript-course/", "rating": 4.7, "duration": "69 hours", "difficulty": "Beginner", "is_free": False, "has_certificate": True, "price": "₹449", "estimated_completion": "2 months"},
        {"title": "JavaScript Tutorial", "provider": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/", "rating": 4.8, "duration": "300 hours", "difficulty": "Beginner", "is_free": True, "has_certificate": True, "price": "Free", "estimated_completion": "3 months"},
    ],
    "react": [
        {"title": "React - The Complete Guide", "provider": "Udemy", "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/", "rating": 4.7, "duration": "68 hours", "difficulty": "Intermediate", "is_free": False, "has_certificate": True, "price": "₹449", "estimated_completion": "2 months"},
        {"title": "Full-Stack Web Development with React", "provider": "Coursera", "url": "https://www.coursera.org/specializations/full-stack-react", "rating": 4.6, "duration": "3 months", "difficulty": "Intermediate", "is_free": True, "has_certificate": True, "price": "Free (Audit)", "estimated_completion": "3 months"},
    ],
    "docker": [
        {"title": "Docker Mastery", "provider": "Udemy", "url": "https://www.udemy.com/course/docker-mastery/", "rating": 4.7, "duration": "20 hours", "difficulty": "Intermediate", "is_free": False, "has_certificate": True, "price": "₹449", "estimated_completion": "3 weeks"},
        {"title": "Docker for Beginners", "provider": "YouTube", "url": "https://www.youtube.com/watch?v=fqMOX6JJhGo", "rating": 4.8, "duration": "3 hours", "difficulty": "Beginner", "is_free": True, "has_certificate": False, "price": "Free", "estimated_completion": "1 day"},
        {"title": "Docker Roadmap", "provider": "Roadmap.sh", "url": "https://roadmap.sh/docker", "rating": 4.9, "duration": "Self-paced", "difficulty": "Beginner", "is_free": True, "has_certificate": False, "price": "Free", "estimated_completion": "2 weeks"},
    ],
    "aws": [
        {"title": "AWS Certified Cloud Practitioner", "provider": "Coursera", "url": "https://www.coursera.org/professional-certificates/aws-cloud-practitioner", "rating": 4.6, "duration": "4 months", "difficulty": "Beginner", "is_free": True, "has_certificate": True, "price": "Free (Audit)", "estimated_completion": "2 months"},
        {"title": "Ultimate AWS Certified Solutions Architect", "provider": "Udemy", "url": "https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/", "rating": 4.7, "duration": "27 hours", "difficulty": "Intermediate", "is_free": False, "has_certificate": True, "price": "₹449", "estimated_completion": "1 month"},
        {"title": "AWS Roadmap", "provider": "Roadmap.sh", "url": "https://roadmap.sh/aws", "rating": 4.9, "duration": "Self-paced", "difficulty": "Intermediate", "is_free": True, "has_certificate": False, "price": "Free", "estimated_completion": "3 months"},
    ],
    "kubernetes": [
        {"title": "Kubernetes for Beginners", "provider": "Udemy", "url": "https://www.udemy.com/course/learn-kubernetes/", "rating": 4.6, "duration": "6 hours", "difficulty": "Beginner", "is_free": False, "has_certificate": True, "price": "₹449", "estimated_completion": "1 week"},
        {"title": "Kubernetes Tutorial", "provider": "YouTube", "url": "https://www.youtube.com/watch?v=X48VuDVv0do", "rating": 4.9, "duration": "4 hours", "difficulty": "Beginner", "is_free": True, "has_certificate": False, "price": "Free", "estimated_completion": "1 day"},
    ],
    "machine learning": [
        {"title": "Machine Learning by Andrew Ng", "provider": "Coursera", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "rating": 4.9, "duration": "3 months", "difficulty": "Intermediate", "is_free": True, "has_certificate": True, "price": "Free (Audit)", "estimated_completion": "3 months"},
        {"title": "Machine Learning with Python", "provider": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/machine-learning-with-python/", "rating": 4.7, "duration": "300 hours", "difficulty": "Intermediate", "is_free": True, "has_certificate": True, "price": "Free", "estimated_completion": "4 months"},
        {"title": "Machine Learning", "provider": "NPTEL", "url": "https://nptel.ac.in/courses/106106139", "rating": 4.5, "duration": "12 weeks", "difficulty": "Intermediate", "is_free": True, "has_certificate": True, "price": "Free", "estimated_completion": "3 months"},
    ],
    "sql": [
        {"title": "The Complete SQL Bootcamp", "provider": "Udemy", "url": "https://www.udemy.com/course/the-complete-sql-bootcamp/", "rating": 4.7, "duration": "9 hours", "difficulty": "Beginner", "is_free": False, "has_certificate": True, "price": "₹449", "estimated_completion": "1 week"},
        {"title": "SQL Tutorial", "provider": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/relational-database/", "rating": 4.8, "duration": "300 hours", "difficulty": "Beginner", "is_free": True, "has_certificate": True, "price": "Free", "estimated_completion": "2 months"},
    ],
    "fastapi": [
        {"title": "FastAPI - The Complete Course", "provider": "Udemy", "url": "https://www.udemy.com/course/completefastapi/", "rating": 4.6, "duration": "20 hours", "difficulty": "Intermediate", "is_free": False, "has_certificate": True, "price": "₹449", "estimated_completion": "3 weeks"},
        {"title": "FastAPI Tutorial", "provider": "YouTube", "url": "https://www.youtube.com/watch?v=7t2alSnE2-I", "rating": 4.8, "duration": "19 hours", "difficulty": "Intermediate", "is_free": True, "has_certificate": False, "price": "Free", "estimated_completion": "2 weeks"},
    ],
    "redis": [
        {"title": "Redis: The Complete Developer's Guide", "provider": "Udemy", "url": "https://www.udemy.com/course/redis-the-complete-developers-guide-p/", "rating": 4.7, "duration": "25 hours", "difficulty": "Intermediate", "is_free": False, "has_certificate": True, "price": "₹449", "estimated_completion": "3 weeks"},
    ],
    "microservices": [
        {"title": "Microservices Architecture", "provider": "Udemy", "url": "https://www.udemy.com/course/microservices-architecture-and-implementation-on-dotnet/", "rating": 4.6, "duration": "28 hours", "difficulty": "Advanced", "is_free": False, "has_certificate": True, "price": "₹449", "estimated_completion": "1 month"},
        {"title": "Microservices Roadmap", "provider": "Roadmap.sh", "url": "https://roadmap.sh/backend", "rating": 4.9, "duration": "Self-paced", "difficulty": "Advanced", "is_free": True, "has_certificate": False, "price": "Free", "estimated_completion": "3 months"},
    ],
    "system design": [
        {"title": "System Design Interview", "provider": "YouTube", "url": "https://www.youtube.com/watch?v=FSR1s2b-l_I", "rating": 4.8, "duration": "Self-paced", "difficulty": "Advanced", "is_free": True, "has_certificate": False, "price": "Free", "estimated_completion": "2 months"},
        {"title": "System Design Roadmap", "provider": "Roadmap.sh", "url": "https://roadmap.sh/system-design", "rating": 4.9, "duration": "Self-paced", "difficulty": "Advanced", "is_free": True, "has_certificate": False, "price": "Free", "estimated_completion": "3 months"},
    ],
}


def recommend_courses_for_skills(missing_skills: list[str]) -> list[dict]:
    """
    Recommend courses for each missing skill.
    Returns list of {skill, courses, learning_path}.
    """
    recommendations = []

    for skill in missing_skills:
        skill_lower = skill.lower().strip()
        courses = COURSE_DATABASE.get(skill_lower, [])

        if not courses:
            # Try partial match
            for key, value in COURSE_DATABASE.items():
                if key in skill_lower or skill_lower in key:
                    courses = value
                    break

        if not courses:
            # Generate generic recommendation
            courses = [{
                "title": f"Learn {skill}",
                "provider": "YouTube",
                "url": f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}+tutorial",
                "rating": 4.5,
                "duration": "Self-paced",
                "difficulty": "Beginner",
                "is_free": True,
                "has_certificate": False,
                "price": "Free",
                "estimated_completion": "2-4 weeks",
            }]

        recommendations.append({
            "skill": skill,
            "courses": courses,
            "learning_path": f"Start with beginner courses → Build projects → Get certified in {skill}",
        })

    return recommendations


def generate_learning_path(user_skills: list[str], target_role: str = None) -> dict:
    """Generate a personalized learning path based on current skills and target role."""
    from services.llm_service import get_llm
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a career development advisor. Create a structured learning path.
Return a JSON object with:
{{
    "target_role": "Role name",
    "estimated_duration": "X months",
    "phases": [
        {{
            "phase": 1,
            "title": "Foundation",
            "duration": "2 weeks",
            "skills_to_learn": ["Skill1", "Skill2"],
            "resources": ["Course/tutorial name"],
            "projects": ["Build a ___"]
        }}
    ],
    "tips": ["Career tip 1", "..."]
}}
Return ONLY valid JSON."""),
        ("human", """Current Skills: {skills}
Target Role: {target_role}
Create a detailed learning roadmap.""")
    ])

    try:
        llm = get_llm()
        chain = prompt | llm
        response = chain.invoke({
            "skills": ", ".join(user_skills[:15]) if user_skills else "None specified",
            "target_role": target_role or "Full Stack Developer",
        })
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        import json
        return json.loads(content)
    except Exception as e:
        return {
            "target_role": target_role or "Full Stack Developer",
            "estimated_duration": "6 months",
            "phases": [
                {
                    "phase": 1,
                    "title": "Foundation",
                    "duration": "1 month",
                    "skills_to_learn": ["Python", "JavaScript", "SQL"],
                    "resources": ["freeCodeCamp", "Coursera"],
                    "projects": ["Build a REST API", "Create a portfolio website"],
                },
                {
                    "phase": 2,
                    "title": "Intermediate",
                    "duration": "2 months",
                    "skills_to_learn": ["React", "FastAPI", "PostgreSQL", "Git"],
                    "resources": ["Udemy", "YouTube tutorials"],
                    "projects": ["Full-stack CRUD app", "Authentication system"],
                },
                {
                    "phase": 3,
                    "title": "Advanced",
                    "duration": "3 months",
                    "skills_to_learn": ["Docker", "AWS", "CI/CD", "System Design"],
                    "resources": ["Roadmap.sh", "Coursera"],
                    "projects": ["Deploy a production app", "Contribute to open source"],
                },
            ],
            "tips": [
                "Build projects consistently",
                "Contribute to open source",
                "Practice system design",
                "Network on LinkedIn",
            ],
        }
