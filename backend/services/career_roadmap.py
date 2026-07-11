"""
TalentSpark AI — AI Career Roadmap Generator
Generates personalized career paths with milestones, skills, and timelines.
"""

import json


# Pre-built roadmap templates for common career paths
CAREER_ROADMAPS = {
    "ai engineer": {
        "title": "AI / Machine Learning Engineer",
        "estimated_duration": "12-18 months",
        "phases": [
            {
                "phase": 1, "title": "🧮 Mathematical Foundations", "duration": "6 weeks",
                "skills": ["Linear Algebra", "Statistics", "Probability", "Calculus"],
                "resources": ["Khan Academy", "3Blue1Brown (YouTube)", "NPTEL Mathematics"],
                "projects": ["Implement linear regression from scratch", "Statistical analysis notebook"],
                "milestone": "Comfortable with math behind ML algorithms"
            },
            {
                "phase": 2, "title": "🐍 Python & Data Science", "duration": "8 weeks",
                "skills": ["Python", "NumPy", "Pandas", "Matplotlib", "Scikit-learn"],
                "resources": ["Python for Data Science (Coursera)", "Kaggle Learn"],
                "projects": ["EDA on real dataset", "Build ML pipeline with scikit-learn"],
                "milestone": "Can build complete ML pipelines"
            },
            {
                "phase": 3, "title": "🧠 Deep Learning", "duration": "10 weeks",
                "skills": ["Neural Networks", "PyTorch/TensorFlow", "CNNs", "RNNs", "Transformers"],
                "resources": ["Deep Learning Specialization (Coursera)", "Fast.ai"],
                "projects": ["Image classifier", "Sentiment analysis model", "Fine-tune a LLM"],
                "milestone": "Can design and train deep learning models"
            },
            {
                "phase": 4, "title": "🤖 LLMs & GenAI", "duration": "8 weeks",
                "skills": ["LangChain", "RAG", "Prompt Engineering", "Vector Databases", "Fine-tuning"],
                "resources": ["LangChain docs", "OpenAI Cookbook", "Hugging Face courses"],
                "projects": ["RAG chatbot", "AI-powered search engine", "Custom fine-tuned model"],
                "milestone": "Can build production LLM applications"
            },
            {
                "phase": 5, "title": "🚀 MLOps & Deployment", "duration": "6 weeks",
                "skills": ["Docker", "MLflow", "AWS SageMaker", "Model monitoring", "CI/CD for ML"],
                "resources": ["MLOps Specialization (Coursera)", "Made With ML"],
                "projects": ["Deploy model to production", "Build ML monitoring dashboard"],
                "milestone": "Can deploy and maintain ML systems in production"
            },
        ]
    },
    "full stack developer": {
        "title": "Full Stack Web Developer",
        "estimated_duration": "8-12 months",
        "phases": [
            {
                "phase": 1, "title": "🌐 Web Fundamentals", "duration": "4 weeks",
                "skills": ["HTML5", "CSS3", "JavaScript (ES6+)", "Responsive Design"],
                "resources": ["freeCodeCamp", "MDN Web Docs", "The Odin Project"],
                "projects": ["Portfolio website", "Responsive landing page"],
                "milestone": "Solid foundation in web technologies"
            },
            {
                "phase": 2, "title": "⚛️ Frontend Framework", "duration": "8 weeks",
                "skills": ["React", "TypeScript", "TailwindCSS", "State Management", "React Router"],
                "resources": ["React docs", "Udemy React Complete Guide", "TypeScript Handbook"],
                "projects": ["Task manager app", "E-commerce UI", "Dashboard with charts"],
                "milestone": "Can build complex, responsive React applications"
            },
            {
                "phase": 3, "title": "🔧 Backend Development", "duration": "8 weeks",
                "skills": ["Python", "FastAPI/Django", "PostgreSQL", "REST APIs", "Authentication"],
                "resources": ["FastAPI docs", "Real Python", "SQLAlchemy tutorial"],
                "projects": ["REST API with auth", "Blog platform backend", "File upload service"],
                "milestone": "Can design and build production APIs"
            },
            {
                "phase": 4, "title": "🔄 Full Stack Integration", "duration": "6 weeks",
                "skills": ["API integration", "Deployment", "Docker", "CI/CD", "Testing"],
                "resources": ["Docker docs", "Vercel/Render guides", "Jest/Pytest"],
                "projects": ["Full-stack app (React + FastAPI)", "Dockerized deployment"],
                "milestone": "Can build and deploy complete web applications"
            },
            {
                "phase": 5, "title": "📈 Advanced Topics", "duration": "6 weeks",
                "skills": ["System Design", "Microservices", "Caching (Redis)", "Message Queues", "GraphQL"],
                "resources": ["System Design Primer", "Roadmap.sh", "Tech blogs"],
                "projects": ["Scalable architecture design", "Real-time chat app"],
                "milestone": "Ready for senior full-stack roles"
            },
        ]
    },
    "devops engineer": {
        "title": "DevOps / Cloud Engineer",
        "estimated_duration": "10-14 months",
        "phases": [
            {
                "phase": 1, "title": "🐧 Linux & Networking", "duration": "4 weeks",
                "skills": ["Linux CLI", "Bash scripting", "Networking (TCP/IP, DNS)", "SSH"],
                "resources": ["Linux Academy", "Roadmap.sh DevOps", "NPTEL Networking"],
                "projects": ["Automate server setup with Bash", "Network monitoring script"],
                "milestone": "Comfortable with Linux administration"
            },
            {
                "phase": 2, "title": "🐳 Containerization", "duration": "6 weeks",
                "skills": ["Docker", "Docker Compose", "Container networking", "Image optimization"],
                "resources": ["Docker Mastery (Udemy)", "Play with Docker"],
                "projects": ["Dockerize multi-service app", "Create custom Docker images"],
                "milestone": "Can containerize any application"
            },
            {
                "phase": 3, "title": "☸️ Orchestration", "duration": "8 weeks",
                "skills": ["Kubernetes", "Helm", "Service mesh", "Auto-scaling", "Monitoring"],
                "resources": ["Kubernetes for Beginners (Udemy)", "CKA prep"],
                "projects": ["Deploy microservices on K8s", "Set up monitoring with Prometheus/Grafana"],
                "milestone": "Can manage Kubernetes clusters"
            },
            {
                "phase": 4, "title": "☁️ Cloud Platforms", "duration": "8 weeks",
                "skills": ["AWS/GCP/Azure", "IAM", "VPC", "S3", "EC2", "Lambda", "RDS"],
                "resources": ["AWS Solutions Architect (Udemy)", "Cloud certifications"],
                "projects": ["Deploy production app on AWS", "Serverless API with Lambda"],
                "milestone": "Cloud certified and deployment-ready"
            },
            {
                "phase": 5, "title": "🔄 CI/CD & IaC", "duration": "6 weeks",
                "skills": ["GitHub Actions", "Jenkins", "Terraform", "Ansible", "GitOps"],
                "resources": ["Terraform docs", "GitHub Actions docs"],
                "projects": ["Full CI/CD pipeline", "Infrastructure as Code with Terraform"],
                "milestone": "Can automate entire deployment lifecycle"
            },
        ]
    },
    "data scientist": {
        "title": "Data Scientist",
        "estimated_duration": "10-14 months",
        "phases": [
            {
                "phase": 1, "title": "📊 Statistics & Python", "duration": "6 weeks",
                "skills": ["Python", "Statistics", "Probability", "NumPy", "Pandas"],
                "resources": ["Statistics (Khan Academy)", "Python for Data Science (Coursera)"],
                "projects": ["Statistical analysis project", "Data cleaning pipeline"],
                "milestone": "Strong statistical and Python foundation"
            },
            {
                "phase": 2, "title": "📈 Data Analysis & Visualization", "duration": "6 weeks",
                "skills": ["Matplotlib", "Seaborn", "Plotly", "SQL", "Tableau/Power BI"],
                "resources": ["Data Visualization (Coursera)", "SQL for Data Science"],
                "projects": ["Interactive dashboard", "Business intelligence report"],
                "milestone": "Can derive insights from complex datasets"
            },
            {
                "phase": 3, "title": "🤖 Machine Learning", "duration": "10 weeks",
                "skills": ["Scikit-learn", "Feature Engineering", "Model Evaluation", "Ensemble Methods"],
                "resources": ["Machine Learning (Coursera - Andrew Ng)", "Kaggle competitions"],
                "projects": ["Predictive model", "Recommendation system", "Kaggle competition"],
                "milestone": "Can build and evaluate ML models"
            },
            {
                "phase": 4, "title": "🧠 Deep Learning & NLP", "duration": "8 weeks",
                "skills": ["Deep Learning", "NLP", "Transformers", "Computer Vision"],
                "resources": ["Deep Learning Specialization", "Hugging Face NLP course"],
                "projects": ["Text classification", "Image recognition system"],
                "milestone": "Can apply deep learning to real problems"
            },
            {
                "phase": 5, "title": "🚀 Production & Communication", "duration": "6 weeks",
                "skills": ["MLOps", "A/B Testing", "Data Storytelling", "Experiment Design"],
                "resources": ["MLOps (Coursera)", "Storytelling with Data (book)"],
                "projects": ["End-to-end ML project", "Data-driven business case study"],
                "milestone": "Ready for data science roles"
            },
        ]
    },
}


def generate_career_roadmap(current_skills: list[str], target_role: str, experience_years: float = 0) -> dict:
    """Generate a personalized career roadmap."""
    target_lower = target_role.lower().strip()

    # Try to find matching template
    template = None
    for key, data in CAREER_ROADMAPS.items():
        if key in target_lower or target_lower in key:
            template = data
            break

    if template:
        # Personalize: mark skills already known
        personalized = _personalize_roadmap(template, current_skills, experience_years)
        return personalized

    # Use LLM for custom roles
    return _generate_custom_roadmap(current_skills, target_role, experience_years)


def _personalize_roadmap(template: dict, current_skills: list[str], experience: float) -> dict:
    """Personalize a roadmap template based on existing skills."""
    current_lower = {s.lower() for s in (current_skills or [])}
    result = {
        "title": template["title"],
        "estimated_duration": template["estimated_duration"],
        "current_skills_count": len(current_skills or []),
        "phases": [],
        "tips": [
            "🎯 Focus on one phase at a time",
            "💻 Build projects to solidify learning",
            "🤝 Join communities (Discord, Reddit, Twitter)",
            "📝 Document your journey (blog/LinkedIn)",
            "🏆 Get certified to validate skills",
        ],
    }

    total_skills_needed = 0
    skills_already_known = 0

    for phase_data in template["phases"]:
        phase_skills = phase_data["skills"]
        known = [s for s in phase_skills if s.lower() in current_lower]
        unknown = [s for s in phase_skills if s.lower() not in current_lower]

        total_skills_needed += len(phase_skills)
        skills_already_known += len(known)

        completion = (len(known) / len(phase_skills) * 100) if phase_skills else 100

        phase = {
            **phase_data,
            "skills_known": known,
            "skills_to_learn": unknown,
            "completion_pct": round(completion, 0),
            "status": "✅ Complete" if completion >= 80 else "🔄 In Progress" if completion > 20 else "⬜ Not Started",
        }

        # Adjust duration based on known skills
        if completion >= 80:
            phase["adjusted_duration"] = "Skip / Review only"
        elif completion >= 50:
            phase["adjusted_duration"] = f"~{int(int(phase_data['duration'].split()[0]) * 0.5)} weeks"
        else:
            phase["adjusted_duration"] = phase_data["duration"]

        result["phases"].append(phase)

    result["overall_readiness"] = round((skills_already_known / max(total_skills_needed, 1)) * 100, 0)
    result["skills_gap_count"] = total_skills_needed - skills_already_known

    return result


def _generate_custom_roadmap(current_skills: list[str], target_role: str, experience: float) -> dict:
    """Generate a custom roadmap using LLM."""
    from services.llm_service import get_llm
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a career development expert. Create a detailed career roadmap.
Return a valid JSON object with this structure:
{{
    "title": "Target Role",
    "estimated_duration": "X months",
    "overall_readiness": 40,
    "phases": [
        {{
            "phase": 1,
            "title": "Phase Name with emoji",
            "duration": "X weeks",
            "skills": ["Skill1", "Skill2"],
            "skills_to_learn": ["Skill1"],
            "skills_known": ["Skill2"],
            "resources": ["Resource1"],
            "projects": ["Project1"],
            "milestone": "Achievement description",
            "completion_pct": 50,
            "status": "🔄 In Progress"
        }}
    ],
    "tips": ["Tip1", "Tip2", "Tip3"]
}}
Create 4-6 phases. Return ONLY valid JSON."""),
        ("human", """Current Skills: {skills}
Target Role: {target_role}
Experience: {experience} years""")
    ])

    try:
        llm = get_llm()
        chain = prompt | llm
        response = chain.invoke({
            "skills": ", ".join(current_skills[:15]) if current_skills else "None",
            "target_role": target_role,
            "experience": experience,
        })
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        print(f"[Career Roadmap] LLM failed: {e}")
        # Fallback to generic roadmap
        return CAREER_ROADMAPS.get("full stack developer", {
            "title": target_role,
            "estimated_duration": "6-12 months",
            "phases": [{"phase": 1, "title": "Learn Fundamentals", "duration": "8 weeks",
                        "skills": ["Core concepts"], "resources": ["Online courses"],
                        "projects": ["Starter project"], "milestone": "Foundation complete"}],
            "tips": ["Build projects consistently", "Network on LinkedIn"],
        })


def get_career_path_options(current_role: str, skills: list[str]) -> list[dict]:
    """Suggest possible career paths based on current role and skills."""
    all_paths = [
        {"role": "AI Engineer", "match_skills": ["python", "machine learning", "deep learning", "nlp"],
         "growth": "Very High", "demand": "🔥 Extremely High", "avg_salary": "18-50 LPA"},
        {"role": "Full Stack Developer", "match_skills": ["react", "node", "python", "sql", "javascript"],
         "growth": "High", "demand": "🔥 Very High", "avg_salary": "10-35 LPA"},
        {"role": "DevOps Engineer", "match_skills": ["docker", "kubernetes", "aws", "linux", "ci/cd"],
         "growth": "High", "demand": "🔥 Very High", "avg_salary": "12-40 LPA"},
        {"role": "Data Scientist", "match_skills": ["python", "statistics", "machine learning", "sql"],
         "growth": "High", "demand": "📈 High", "avg_salary": "12-45 LPA"},
        {"role": "Cloud Architect", "match_skills": ["aws", "azure", "gcp", "terraform", "networking"],
         "growth": "Very High", "demand": "📈 High", "avg_salary": "20-60 LPA"},
        {"role": "Product Manager", "match_skills": ["analytics", "communication", "strategy"],
         "growth": "High", "demand": "📈 High", "avg_salary": "15-50 LPA"},
        {"role": "Mobile Developer", "match_skills": ["react native", "flutter", "swift", "kotlin"],
         "growth": "Moderate", "demand": "📊 Moderate", "avg_salary": "8-35 LPA"},
        {"role": "Cybersecurity Analyst", "match_skills": ["networking", "linux", "security", "python"],
         "growth": "Very High", "demand": "🔥 Very High", "avg_salary": "10-40 LPA"},
    ]

    user_skills_lower = {s.lower() for s in (skills or [])}
    for path in all_paths:
        matching = [s for s in path["match_skills"] if s in user_skills_lower]
        path["skills_match_pct"] = round((len(matching) / max(len(path["match_skills"]), 1)) * 100)
        path["matching_skills"] = matching
        path["skills_needed"] = [s for s in path["match_skills"] if s not in user_skills_lower]

    # Sort by match percentage
    all_paths.sort(key=lambda x: x["skills_match_pct"], reverse=True)
    return all_paths
