import re

from utils.validators import extract_known_skills, normalize_skills


EXPERIENCE_PATTERNS = [
    r"(\d+\+?\s*years?\s+of\s+experience)",
    r"experience\s*:\s*([^\n\.]+)",
]


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

    keywords = sorted(set(re.findall(r"[A-Za-z][A-Za-z\+\.#]{2,}", jd_text.lower())))
    keyword_gaps = [k for k in keywords[:120] if k in jd_skills and k not in resume_skills]

    return {
        "required_skills": jd_skills,
        "required_experience": experience_req,
        "technologies": jd_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "keyword_gap": keyword_gaps,
        "match_percentage": match_percentage,
    }
