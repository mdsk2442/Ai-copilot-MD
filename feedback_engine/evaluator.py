from utils.gemini_integration import generate_json


def evaluate_answers(role: str, questions: list[str], answers: list[str]) -> dict:
    pairs = [{"question": q, "answer": a} for q, a in zip(questions, answers)]
    answered = [a for a in answers if a and a.strip()]
    avg_len = sum(len(a.split()) for a in answered) / max(len(answered), 1)

    heuristic = {
        "technical": min(100, int(avg_len * 2.2)),
        "communication": min(100, int(avg_len * 2.0)),
        "clarity": min(100, 55 + len(answered) * 4),
        "confidence": min(100, 50 + len(answered) * 5),
        "problem_solving": min(100, int(avg_len * 1.8)),
    }
    heuristic["overall"] = int(sum(heuristic.values()) / len(heuristic))

    prompt = f"""
    Evaluate interview answers for a {role} role.
    Q/A pairs: {pairs}
    Return JSON with scores object (technical, communication, clarity, confidence, problem_solving, overall), strengths, weaknesses, improvement_areas, feedback.
    """

    fallback = {
        "scores": heuristic,
        "strengths": ["Good response coverage", "Consistent participation"],
        "weaknesses": ["Some answers can be more specific"],
        "improvement_areas": ["Use measurable achievements", "Add structured examples"],
        "feedback": "Solid baseline performance with room to improve depth and specificity.",
    }

    data = generate_json(prompt, default=fallback)
    scores = data.get("scores") if isinstance(data.get("scores"), dict) else heuristic
    for key in ["technical", "communication", "clarity", "confidence", "problem_solving", "overall"]:
        scores[key] = int(max(0, min(100, int(scores.get(key, heuristic[key])))))

    return {
        "scores": scores,
        "strengths": data.get("strengths", fallback["strengths"]),
        "weaknesses": data.get("weaknesses", fallback["weaknesses"]),
        "improvement_areas": data.get("improvement_areas", fallback["improvement_areas"]),
        "feedback": data.get("feedback", fallback["feedback"]),
    }
