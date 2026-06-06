from datetime import UTC, datetime

import pandas as pd


def create_interview_session_payload(user_id, resume_id, role: str, questions: list[str], answers: list[str], evaluation: dict) -> dict:
    return {
        "user_id": user_id,
        "resume_id": resume_id,
        "role": role,
        "questions": questions,
        "answers": answers,
        "scores": evaluation.get("scores", {}),
        "feedback": evaluation.get("feedback", ""),
        "created_at": datetime.now(UTC),
    }


def reports_to_dataframe(sessions: list[dict]) -> pd.DataFrame:
    rows = []
    for session in sessions:
        rows.append(
            {
                "Date": session.get("created_at"),
                "Role": session.get("role"),
                "Overall Score": session.get("scores", {}).get("overall", 0),
                "Technical": session.get("scores", {}).get("technical", 0),
                "Communication": session.get("scores", {}).get("communication", 0),
                "Feedback": session.get("feedback", ""),
            }
        )
    return pd.DataFrame(rows)


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")
