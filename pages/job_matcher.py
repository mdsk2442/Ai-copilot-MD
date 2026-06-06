import streamlit as st
from bson import ObjectId

from jd_matcher.matcher import analyze_job_description


def render(db, user_id):
    st.subheader("Job Description Analyzer")
    jd_text = st.text_area("Paste Job Description", height=260)

    resumes = list(db.resumes.find({"user_id": ObjectId(user_id)}).sort("created_at", -1).limit(20))
    if not resumes:
        st.info("Upload a resume first to run JD matching.")
        return

    options = {f"{r.get('file_name', 'resume')} ({str(r['_id'])[:8]})": r for r in resumes}
    selected = st.selectbox("Select Resume", options=list(options.keys()))

    if st.button("Analyze Match", type="primary"):
        resume = options[selected]
        analysis = analyze_job_description(jd_text, resume)

        db.job_descriptions.insert_one(
            {
                "user_id": ObjectId(user_id),
                "title": "Pasted JD",
                "description": jd_text,
                "required_skills": analysis["required_skills"],
                "required_experience": analysis["required_experience"],
                "technologies": analysis["technologies"],
            }
        )

        st.session_state["latest_match"] = analysis["match_percentage"]
        st.metric("Resume Match Score", f"{analysis['match_percentage']}%")
        c1, c2 = st.columns(2)
        c1.write("**Matched Skills**")
        c1.write("\n".join([f"✓ {s}" for s in analysis["matched_skills"]]) or "- None")
        c2.write("**Missing Skills**")
        c2.write("\n".join([f"✗ {s}" for s in analysis["missing_skills"]]) or "- None")

        with st.expander("Detailed Analysis"):
            st.json(analysis)
