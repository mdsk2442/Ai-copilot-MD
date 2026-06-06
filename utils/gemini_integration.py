import json
import os
from typing import Any

from utils.logger import get_logger

logger = get_logger(__name__)


def _configure() -> bool:
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return False
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        return True
    except Exception as exc:
        logger.warning("Gemini configuration failed: %s", exc)
        return False


def generate_text(prompt: str, default: str = "") -> str:
    if not _configure():
        return default
    try:
        import google.generativeai as genai

        model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))
        response = model.generate_content(prompt)
        return (response.text or "").strip() or default
    except Exception as exc:
        logger.warning("Gemini text generation failed: %s", exc)
        return default


def generate_json(prompt: str, default: dict[str, Any]) -> dict[str, Any]:
    response = generate_text(
        prompt + "\nReturn valid JSON only.",
        default=json.dumps(default),
    )
    try:
        data = json.loads(response)
        return data if isinstance(data, dict) else default
    except Exception:
        return default
