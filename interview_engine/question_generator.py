from utils.gemini_integration import generate_json

CATEGORIES = ["HR", "Technical", "Project", "Behavioral", "Scenario"]


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

    fallback = {
        category: [f"{category} {difficulty} question {i+1} for {role}" for i in range(10)]
        for category in CATEGORIES
    }

    data = generate_json(prompt, default=fallback)
    out = {}
    for category in CATEGORIES:
        questions = data.get(category) if isinstance(data.get(category), list) else fallback[category]
        out[category] = [str(q) for q in questions[:10]]
        if len(out[category]) < 10:
            out[category] += fallback[category][len(out[category]):10]
    return out
