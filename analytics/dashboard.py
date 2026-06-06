from collections import Counter

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def build_cards(latest_ats: int = 0, latest_interview: int = 0, match_score: int = 0) -> dict:
    readiness = int((latest_ats + latest_interview + match_score) / 3) if any([latest_ats, latest_interview, match_score]) else 0
    return {
        "ATS Score": latest_ats,
        "Interview Score": latest_interview,
        "Resume Match Score": match_score,
        "Skill Readiness Score": readiness,
    }


def ats_trend_chart(ats_scores: list[int]) -> go.Figure:
    df = pd.DataFrame({"Attempt": list(range(1, len(ats_scores) + 1)), "ATS Score": ats_scores or [0]})
    return px.line(df, x="Attempt", y="ATS Score", markers=True, title="ATS Trend")


def interview_trend_chart(interview_scores: list[int]) -> go.Figure:
    df = pd.DataFrame({"Session": list(range(1, len(interview_scores) + 1)), "Interview Score": interview_scores or [0]})
    return px.line(df, x="Session", y="Interview Score", markers=True, title="Interview Performance Trend")


def skill_distribution_chart(skills: list[str]) -> go.Figure:
    if not skills:
        return px.bar(pd.DataFrame({"Skill": [], "Count": []}), x="Skill", y="Count", title="Skill Distribution")
    counts = Counter(skills)
    df = pd.DataFrame({"Skill": list(counts.keys()), "Count": list(counts.values())})
    return px.bar(df, x="Skill", y="Count", title="Skill Distribution")


def readiness_progress_chart(ats_scores: list[int], interview_scores: list[int]) -> go.Figure:
    n = max(len(ats_scores), len(interview_scores), 1)
    ats = ats_scores + [ats_scores[-1] if ats_scores else 0] * (n - len(ats_scores))
    iv = interview_scores + [interview_scores[-1] if interview_scores else 0] * (n - len(interview_scores))
    readiness = [int((a + i) / 2) for a, i in zip(ats, iv)]
    df = pd.DataFrame({"Stage": list(range(1, n + 1)), "Readiness": readiness})
    return px.area(df, x="Stage", y="Readiness", title="Readiness Progress")
