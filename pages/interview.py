import streamlit as st
from bson import ObjectId

from feedback_engine.evaluator import evaluate_answers
from interview_engine.question_generator import generate_questions
from reports.generator import create_interview_session_payload

ROLES = ["Software Engineer", "Data Analyst", "Frontend Developer", "Backend Developer", "Full Stack Developer"]
MAX_INTERVIEW_QUESTIONS = 15


def render(db, user_id):
    st.subheader("AI Mock Interview")

    resumes = list(db.resumes.find({"user_id": ObjectId(user_id)}).sort("created_at", -1).limit(20))
    if not resumes:
        st.info("Upload a resume before starting interviews.")
        return

    labels = {f"{r.get('file_name', 'resume')} ({str(r['_id'])[:8]})": r for r in resumes}
    selected_label = st.selectbox("Select Resume", list(labels.keys()))
    selected_resume = labels[selected_label]

    role = st.selectbox("Target Role", ROLES)
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=1)
    jd_text = st.text_area("Optional Job Description Context", height=140)

    if st.button("Generate Interview Questions", type="primary"):
        question_map = generate_questions(selected_resume, jd_text, role, difficulty)
        st.session_state["question_map"] = question_map
        st.success("Questions generated.")

    question_map = st.session_state.get("question_map")
    if not question_map:
        return

    st.markdown("### Interview Questions")
    all_questions = []
    for category, questions in question_map.items():
        st.markdown(f"**{category}**")
        for q in questions:
            st.write(f"- {q}")
        all_questions.extend(questions)

    with st.form("answer_form"):
        st.markdown("### Submit Answers")
        answers = []
        for i, q in enumerate(all_questions[:MAX_INTERVIEW_QUESTIONS], start=1):
            answers.append(st.text_area(f"Q{i}: {q}", height=80))
        submitted = st.form_submit_button("Evaluate Answers")

    if submitted:
        evaluation = evaluate_answers(role, all_questions[:MAX_INTERVIEW_QUESTIONS], answers)
        payload = create_interview_session_payload(
            ObjectId(user_id),
            selected_resume["_id"],
            role,
            all_questions[:MAX_INTERVIEW_QUESTIONS],
            answers,
            evaluation,
        )
        db.interview_sessions.insert_one(payload)
        st.session_state["latest_interview"] = evaluation["scores"]["overall"]

        st.metric("Overall Interview Score", f"{evaluation['scores']['overall']} / 100")
        st.json(evaluation["scores"])
        st.write("**Strengths**")
        st.write("\n".join([f"- {x}" for x in evaluation["strengths"]]))
        st.write("**Weaknesses**")
        st.write("\n".join([f"- {x}" for x in evaluation["weaknesses"]]))
        st.write("**Improvement Areas**")
        st.write("\n".join([f"- {x}" for x in evaluation["improvement_areas"]]))
        st.write("**Feedback**")
        st.write(evaluation["feedback"])
