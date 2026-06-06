import re
import tempfile
from datetime import UTC, datetime
import os
from pathlib import Path

from resume_parser.docx_parser import extract_docx_text
from resume_parser.pdf_parser import extract_pdf_text
from utils.validators import extract_known_skills, normalize_skills

SECTION_PATTERNS = {
    "education": ["education", "academic"],
    "experience": ["experience", "work history", "employment"],
    "projects": ["projects"],
    "certifications": ["certifications", "certificates"],
}


def _extract_section_lines(text: str, keywords: list[str]) -> list[str]:
    lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
    out: list[str] = []
    capture = False
    for line in lines:
        lower = line.lower().strip(":")
        if any(k in lower for k in keywords):
            capture = True
            continue
        if capture and any(token in lower for token in ["education", "experience", "projects", "certifications", "skills"]):
            capture = False
        elif capture:
            out.append(line)
    return out[:12]


def extract_resume_entities(text: str) -> dict:
    email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text or "")
    phone = re.search(r"(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{3}\)?[\s-]?)?\d{3}[\s-]?\d{4}", text or "")

    lines = [ln.strip() for ln in (text or "").splitlines() if ln.strip()]
    name = lines[0] if lines else "Unknown"

    skills_guess = normalize_skills(re.split(r"[,|•\-]", " ".join(_extract_section_lines(text, ["skills", "tech stack"]))))
    skills = normalize_skills(skills_guess + extract_known_skills(text))

    return {
        "name": name,
        "email": email.group(0) if email else "",
        "phone": phone.group(0) if phone else "",
        "education": _extract_section_lines(text, SECTION_PATTERNS["education"]),
        "skills": skills,
        "experience": _extract_section_lines(text, SECTION_PATTERNS["experience"]),
        "projects": _extract_section_lines(text, SECTION_PATTERNS["projects"]),
        "certifications": _extract_section_lines(text, SECTION_PATTERNS["certifications"]),
    }


def parse_resume_file(uploaded_file) -> dict:
    suffix = Path(uploaded_file.name).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        path = tmp.name

    try:
        text = ""
        if suffix == ".pdf":
            text = extract_pdf_text(path)
        elif suffix == ".docx":
            text = extract_docx_text(path)
        else:
            raise ValueError("Only PDF and DOCX are supported")
    finally:
        if os.path.exists(path):
            os.unlink(path)

    entities = extract_resume_entities(text)
    entities["file_name"] = uploaded_file.name
    entities["raw_text"] = text
    entities["created_at"] = datetime.now(UTC)
    entities["updated_at"] = datetime.now(UTC)
    return entities
