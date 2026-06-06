import os

import streamlit as st

from auth.user_manager import UserManager
from database.models import DatabaseManager
from pages import analytics, dashboard, interview, job_matcher, resume_analyzer

st.set_page_config(page_title="AI Career Intelligence Platform", page_icon="🎯", layout="wide")


def load_css(path: str = "assets/styles.css"):
    try:
        with open(path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


def render_auth(user_manager: UserManager):
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login")
        if login_btn:
            ok, token, user = user_manager.login(email, password)
            if ok:
                st.session_state["token"] = token
                st.session_state["user"] = user
                st.success("Login successful")
                st.rerun()
            else:
                st.error(token)

    with tab2:
        with st.form("register_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            register_btn = st.form_submit_button("Create Account")
        if register_btn:
            ok, message = user_manager.register(name, email, password)
            if ok:
                st.success(message)
            else:
                st.error(message)


def render_app(db: DatabaseManager, user_manager: UserManager):
    user = st.session_state.get("user")
    if not user:
        render_auth(user_manager)
        return

    st.sidebar.title("AI Career Intelligence")
    st.sidebar.write(f"Logged in as **{user['name']}**")

    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Resume Analyzer", "Job Matcher", "Mock Interview", "Analytics & Reports"],
    )

    with st.sidebar.expander("Profile"):
        phone = st.text_input("Phone", value="")
        profile_picture = st.text_input("Profile Picture URL", value="")
        if st.button("Save Profile"):
            ok, msg = user_manager.update_profile(user["id"], phone=phone, profile_picture=profile_picture)
            st.success(msg) if ok else st.error(msg)

    if st.sidebar.button("Logout"):
        for key in ["token", "user", "question_map", "active_resume_id", "latest_ats", "latest_interview", "latest_match"]:
            st.session_state.pop(key, None)
        st.rerun()

    if page == "Dashboard":
        dashboard.render()
    elif page == "Resume Analyzer":
        resume_analyzer.render(db, user["id"])
    elif page == "Job Matcher":
        job_matcher.render(db, user["id"])
    elif page == "Mock Interview":
        interview.render(db, user["id"])
    elif page == "Analytics & Reports":
        analytics.render(db, user["id"])


def main():
    if not os.getenv("JWT_SECRET"):
        st.error("JWT_SECRET is not configured. Please set it in environment variables before running the app.")
        st.stop()
    load_css()
    db = DatabaseManager()
    user_manager = UserManager(db)
    render_app(db, user_manager)


if __name__ == "__main__":
    main()
