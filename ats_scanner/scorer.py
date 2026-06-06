from collections import Counter

from utils.gemini_integration import generate_text

MAX_SKILLS_FOR_AI_PROMPT = 20


def calculate_ats_score(resume: dict, jd_text: str = "") -> dict:
    strengths: list[str] = []
    weaknesses: list[str] = []

    contact_score = 12 if resume.get("email") and resume.get("phone") else 6
    if contact_score == 12:
        strengths.append("Contact information is complete")
    else:
        weaknesses.append("Add both professional email and phone number")

    section_count = sum(1 for key in ["education", "experience", "projects", "skills", "certifications"] if resume.get(key))
    section_score = min(section_count * 8, 28)
    if section_count >= 4:
        strengths.append("Resume has strong section completeness")
    else:
        weaknesses.append("Add missing key sections (education/experience/projects)")

    skills = [s.lower() for s in resume.get("skills", [])]
    skills_score = min(len(skills) * 2, 20)
    if len(skills) >= 8:
        strengths.append("Skill coverage is strong")
    else:
        weaknesses.append("Add more role-relevant tools and technologies")

    words = (resume.get("raw_text", "") or "").split()
    readability_score = 20 if 250 <= len(words) <= 900 else 12

    keyword_score = 0
    if jd_text.strip():
        jd_words = [w.strip(".,:;()[]{}").lower() for w in jd_text.split() if len(w) > 2]
        common = Counter(jd_words)
        hits = sum(1 for token in set(skills) if token in common)
        keyword_score = min(hits * 4, 20)
        if hits >= 3:
            strengths.append("Resume aligns with job keywords")
        else:
            weaknesses.append("Improve keyword alignment with the target job description")
    else:
        keyword_score = 10

    total = int(min(contact_score + section_score + skills_score + readability_score + keyword_score, 100))

    safe_resume_summary = {
        "skills": skills[:MAX_SKILLS_FOR_AI_PROMPT],
        "education_count": len(resume.get("education", [])),
        "experience_count": len(resume.get("experience", [])),
        "projects_count": len(resume.get("projects", [])),
        "certifications_count": len(resume.get("certifications", [])),
        "ats_score": total,
    }
    ai_suggestions = generate_text(
        f"Provide 3 concise ATS improvement suggestions for this resume summary: {safe_resume_summary}",
        default="1) Quantify project impact.\n2) Align keywords with target role.\n3) Improve section clarity.",
    )

    return {
        "ats_score": total,
        "metrics": {
            "contact_information": contact_score,
            "section_completeness": section_score,
            "skills_presence": skills_score,
            "readability": readability_score,
            "keyword_relevance": keyword_score,
        },
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": ai_suggestions,
    }
