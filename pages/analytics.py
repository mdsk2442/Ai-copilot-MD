import streamlit as st
from bson import ObjectId

from analytics.dashboard import ats_trend_chart, interview_trend_chart, readiness_progress_chart, skill_distribution_chart
from reports.generator import dataframe_to_csv_bytes, reports_to_dataframe


def render(db, user_id):
    st.subheader("Analytics & Interview Reports")

    resumes = list(db.resumes.find({"user_id": ObjectId(user_id)}).sort("created_at", 1))
    sessions = list(db.interview_sessions.find({"user_id": ObjectId(user_id)}).sort("created_at", 1))

    ats_scores = [int(r.get("ats_score", 0)) for r in resumes]
    interview_scores = [int(s.get("scores", {}).get("overall", 0)) for s in sessions]
    all_skills = []
    for resume in resumes:
        all_skills.extend(resume.get("skills", []))

    c1, c2 = st.columns(2)
    c1.plotly_chart(ats_trend_chart(ats_scores), use_container_width=True)
    c2.plotly_chart(interview_trend_chart(interview_scores), use_container_width=True)

    c3, c4 = st.columns(2)
    c3.plotly_chart(skill_distribution_chart(all_skills), use_container_width=True)
    c4.plotly_chart(readiness_progress_chart(ats_scores, interview_scores), use_container_width=True)

    st.markdown("### Interview Reports")
    if not sessions:
        st.info("No interview sessions available yet.")
        return

    df = reports_to_dataframe(sessions)
    st.dataframe(df, use_container_width=True)
    st.download_button("Download Reports (CSV)", data=dataframe_to_csv_bytes(df), file_name="interview_reports.csv", mime="text/csv")
