import re
from typing import Iterable

COMMON_SKILLS = {
    "python", "java", "javascript", "typescript", "sql", "mongodb", "postgresql",
    "mysql", "docker", "kubernetes", "aws", "azure", "gcp", "react", "next.js",
    "fastapi", "django", "flask", "streamlit", "pandas", "numpy", "scikit-learn",
    "power bi", "tableau", "git", "redis", "html", "css", "node.js", "linux",
}
PASSWORD_SPECIALS = set("!@#$%^&*()-_=+[]{}|;:,.<>?/~`")


def is_valid_email(email: str) -> bool:
    email = (email or "").strip()
    if not email or "@" not in email or email.count("@") != 1:
        return False
    local, domain = email.split("@")
    if not local or not domain or "." not in domain:
        return False
    if any(part == "" for part in domain.split(".")):
        return False
    return len(email) <= 254


def is_strong_password(password: str) -> bool:
    if not password or len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in PASSWORD_SPECIALS for c in password)
    return has_upper and has_lower and has_digit and has_special


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
