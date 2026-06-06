import streamlit as st

from analytics.dashboard import build_cards


def render():
    st.subheader("Career Intelligence Dashboard")
    latest_ats = st.session_state.get("latest_ats", 0)
    latest_interview = st.session_state.get("latest_interview", 0)
    latest_match = st.session_state.get("latest_match", 0)

    cards = build_cards(latest_ats, latest_interview, latest_match)
    cols = st.columns(4)
    for (label, value), col in zip(cards.items(), cols):
        col.metric(label, f"{value}%")

    st.markdown("---")
    st.write("Welcome to your AI-powered career workspace. Use the sidebar to analyze resumes, match jobs, and practice interviews.")
