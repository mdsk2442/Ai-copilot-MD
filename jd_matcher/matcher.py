import re

from utils.validators import extract_known_skills, normalize_skills


EXPERIENCE_PATTERNS = [
    r"(\d+\+?\s*years?\s+of\s+experience)",
    r"experience\s*:\s*([^\n\.]+)",
]
MAX_KEYWORDS = 120


def analyze_job_description(jd_text: str, resume: dict) -> dict:
    jd_skills = extract_known_skills(jd_text)
    resume_skills = normalize_skills(resume.get("skills", []))

    matched = sorted(set(jd_skills) & set(resume_skills))
    missing = sorted(set(jd_skills) - set(resume_skills))

    match_percentage = int((len(matched) / max(len(jd_skills), 1)) * 100)

    experience_req = "Not specified"
    for pattern in EXPERIENCE_PATTERNS:
        m = re.search(pattern, jd_text, flags=re.IGNORECASE)
        if m:
            experience_req = m.group(1)
            break

    keyword_gaps = [skill for skill in jd_skills if skill not in resume_skills][:MAX_KEYWORDS]

    return {
        "required_skills": jd_skills,
        "required_experience": experience_req,
        "technologies": jd_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "keyword_gap": keyword_gaps,
        "match_percentage": match_percentage,
    }
