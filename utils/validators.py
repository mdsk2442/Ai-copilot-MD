import re
from typing import Iterable

COMMON_SKILLS = {
    "python", "java", "javascript", "typescript", "sql", "mongodb", "postgresql",
    "mysql", "docker", "kubernetes", "aws", "azure", "gcp", "react", "next.js",
    "fastapi", "django", "flask", "streamlit", "pandas", "numpy", "scikit-learn",
    "power bi", "tableau", "git", "redis", "html", "css", "node.js", "linux",
}


def is_valid_email(email: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email or ""))


def is_strong_password(password: str) -> bool:
    if not password or len(password) < 8:
        return False
    return any(c.isupper() for c in password) and any(c.islower() for c in password) and any(c.isdigit() for c in password)


def normalize_skills(skills: Iterable[str]) -> list[str]:
    normalized = []
    seen = set()
    for skill in skills:
        s = (skill or "").strip().lower()
        if not s:
            continue
        if s not in seen:
            seen.add(s)
            normalized.append(s)
    return normalized


def extract_known_skills(text: str) -> list[str]:
    text_l = (text or "").lower()
    return sorted([s for s in COMMON_SKILLS if s in text_l])
