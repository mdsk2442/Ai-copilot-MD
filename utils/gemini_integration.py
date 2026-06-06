import json
import os
from typing import Any

from utils.logger import get_logger

logger = get_logger(__name__)
_GEMINI_READY: bool | None = None


def _configure() -> bool:
    global _GEMINI_READY
    if _GEMINI_READY is not None:
        return _GEMINI_READY
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        _GEMINI_READY = False
        return False
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        _GEMINI_READY = True
        return True
    except Exception as exc:
        logger.warning("Gemini configuration failed: %s", exc)
        _GEMINI_READY = False
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
