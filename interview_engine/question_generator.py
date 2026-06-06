from utils.gemini_integration import generate_json

CATEGORIES = ["HR", "Technical", "Project", "Behavioral", "Scenario"]


def _fallback_questions(role: str, difficulty: str, resume: dict) -> dict:
    resume_skills = [str(s).strip() for s in resume.get("skills", []) if str(s).strip()]
    technical_skills = (resume_skills[:10] if resume_skills else ["Python", "SQL", "APIs", "Data Structures", "System Design", "Testing", "Debugging", "Performance", "Security", "Version Control"])
    return {
        "HR": [
            f"Tell me about yourself for the {role} position.",
            "Why do you want this role?",
            "What are your strongest professional qualities?",
            "Describe a challenge you handled at work or in academics.",
            "How do you prioritize work under deadlines?",
            "What motivates you to keep learning?",
            "How do you handle feedback from peers or managers?",
            "Describe a time you worked in a team.",
            "Where do you see your career in the next 3 years?",
            f"What makes you a strong {difficulty.lower()}-level candidate?",
        ],
        "Technical": [f"Explain {skill} fundamentals relevant to {role}." for skill in technical_skills],
        "Project": [
            "Describe your most impactful project and your contribution.",
            "What architecture choices did you make and why?",
            "How did you validate project requirements?",
            "What trade-offs did you face during implementation?",
            "How did you test and monitor your project?",
            "What would you improve if you rebuilt the project?",
            "How did your project deliver measurable impact?",
            "How did you handle failures or bugs in production-like environments?",
            "How did you collaborate across teams on project delivery?",
            "Which tools accelerated your delivery and why?",
        ],
        "Behavioral": [
            "Tell me about a time you resolved a conflict in a team.",
            "Describe a situation where you had to learn quickly.",
            "Share an example of taking ownership without being asked.",
            "Describe a decision you made with limited information.",
            "How have you handled ambiguous requirements?",
            "Tell me about a time you missed a goal and what you learned.",
            "Describe how you mentor or support peers.",
            "How do you maintain consistency during long projects?",
            "Describe a time when communication changed an outcome.",
            "How do you react when priorities shift suddenly?",
        ],
        "Scenario": [
            "How would you approach a failing production deployment?",
            "How would you improve a slow database query pipeline?",
            "How would you design a feature for high traffic growth?",
            "How would you debug inconsistent API responses?",
            "How would you handle missing stakeholder requirements?",
            "How would you secure user data in a web application?",
            "How would you recover from accidental data loss?",
            "How would you estimate and plan an unfamiliar feature?",
            "How would you balance speed and quality under pressure?",
            "How would you communicate risks to non-technical stakeholders?",
        ],
    }


def generate_questions(resume: dict, jd_text: str, role: str, difficulty: str = "Medium") -> dict:
    prompt = f"""
    Create interview questions using this context.
    Role: {role}
    Difficulty: {difficulty}
    Resume skills: {resume.get('skills', [])}
    Resume projects: {resume.get('projects', [])}
    Job description: {jd_text}

    Generate JSON with keys HR, Technical, Project, Behavioral, Scenario.
    Each key should have at least 10 short questions.
    """

    fallback = _fallback_questions(role, difficulty, resume)

    data = generate_json(prompt, default=fallback)
    out = {}
    for category in CATEGORIES:
        questions = data.get(category) if isinstance(data.get(category), list) else fallback[category]
        out[category] = [str(q) for q in questions[:10]]
        if len(out[category]) < 10:
            out[category] += fallback[category][len(out[category]):10]
    return out
