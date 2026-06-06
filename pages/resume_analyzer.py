import streamlit as st
from bson import ObjectId

from ats_scanner.scorer import calculate_ats_score
from resume_parser.extraction import parse_resume_file


def render(db, user_id):
    st.subheader("Resume Analyzer")
    uploaded = st.file_uploader("Upload your resume (PDF/DOCX)", type=["pdf", "docx"])
    jd_context = st.text_area("Optional target Job Description for ATS optimization", height=160)

    if uploaded and st.button("Parse Resume & Calculate ATS", type="primary"):
        try:
            parsed = parse_resume_file(uploaded)
            ats = calculate_ats_score(parsed, jd_context)
            parsed.update({"user_id": ObjectId(user_id), "ats_score": ats["ats_score"]})
            result = db.resumes.insert_one(parsed)

            st.session_state["active_resume_id"] = str(result.inserted_id)
            st.session_state["latest_ats"] = ats["ats_score"]
            st.success("Resume parsed and saved successfully")

            st.metric("ATS Score", f"{ats['ats_score']} / 100")
            st.json(ats["metrics"])
            st.write("**Strengths**")
            st.write("\n".join([f"- {x}" for x in ats["strengths"]]) or "- N/A")
            st.write("**Weaknesses**")
            st.write("\n".join([f"- {x}" for x in ats["weaknesses"]]) or "- N/A")
            st.write("**Suggestions**")
            st.write(ats["suggestions"])

            with st.expander("Extracted Resume Data", expanded=False):
                st.json({k: v for k, v in parsed.items() if k != "raw_text"})
        except Exception as exc:
            st.error(f"Failed to process resume: {exc}")
