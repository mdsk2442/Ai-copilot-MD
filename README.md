# AI Career Intelligence Platform

Production-ready Streamlit platform for resume intelligence, ATS analysis, JD matching, AI mock interviews, feedback scoring, and interview readiness analytics.

## Features

- JWT authentication with bcrypt password hashing
- Resume parser for PDF and DOCX
- ATS scanner with detailed scoring metrics
- Job description analyzer with skill matching and gap analysis
- Skill gap and readiness tracking
- AI interview question generation (Gemini with fallback)
- AI feedback engine with multi-factor scoring
- Analytics dashboard with Plotly charts
- Interview session history + CSV report download
- MongoDB Atlas free-tier compatible schema/index setup

## Tech Stack

- Frontend/UI: Streamlit, custom CSS, Plotly
- Backend: Python 3.12 modular architecture
- Database: MongoDB Atlas (free tier)
- Auth: JWT + bcrypt
- AI: Gemini API (free tier) with prompt engineering and resume-context prompting

## Project Structure

```text
project/
├── app.py
├── auth/
│   ├── __init__.py
│   ├── jwt_handler.py
│   ├── password_hash.py
│   └── user_manager.py
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── models.py
├── resume_parser/
│   ├── __init__.py
│   ├── pdf_parser.py
│   ├── docx_parser.py
│   └── extraction.py
├── ats_scanner/
│   ├── __init__.py
│   └── scorer.py
├── jd_matcher/
│   ├── __init__.py
│   └── matcher.py
├── interview_engine/
│   ├── __init__.py
│   └── question_generator.py
├── feedback_engine/
│   ├── __init__.py
│   └── evaluator.py
├── analytics/
│   ├── __init__.py
│   └── dashboard.py
├── reports/
│   ├── __init__.py
│   └── generator.py
├── utils/
│   ├── __init__.py
│   ├── gemini_integration.py
│   ├── logger.py
│   └── validators.py
├── assets/
│   ├── styles.css
│   └── icons/
├── pages/
│   ├── dashboard.py
│   ├── resume_analyzer.py
│   ├── job_matcher.py
│   ├── interview.py
│   └── analytics.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

## MongoDB Collections

### users
- `_id`, `name`, `email` (unique), `password_hash`, `created_at`, `last_login`, `profile_picture`, `phone`

### resumes
- `_id`, `user_id`, `file_name`, `name`, `email`, `phone`, `education`, `skills`, `experience`, `projects`, `certifications`, `ats_score`, `raw_text`, `created_at`, `updated_at`

### interview_sessions
- `_id`, `user_id`, `resume_id`, `role`, `questions`, `answers`, `scores` (`technical`, `communication`, `clarity`, `confidence`, `problem_solving`, `overall`), `feedback`, `created_at`

### job_descriptions
- `_id`, `user_id`, `title`, `description`, `required_skills`, `required_experience`, `technologies`, `created_at`

### analytics
- `_id`, `user_id`, `ats_scores`, `interview_scores`, `skill_improvements`, `created_at`

## Local Setup

1. **Create and activate a virtual env**
   - `python -m venv .venv`
   - `source .venv/bin/activate` (Linux/macOS) or `.venv\\Scripts\\activate` (Windows)

2. **Install dependencies**
   - `pip install -r requirements.txt`

3. **Configure environment**
   - Copy `.env.example` to `.env`
   - Set `MONGODB_URI`, `JWT_SECRET`, and `GEMINI_API_KEY`

4. **Run app**
   - `streamlit run app.py`

## Streamlit Community Cloud Deployment

1. Push repository to GitHub.
2. Open Streamlit Community Cloud and create app from this repo.
3. Set main file path to `app.py`.
4. Add secrets in Streamlit settings:
   - `MONGODB_URI`
   - `MONGODB_DB_NAME`
   - `JWT_SECRET`
   - `JWT_EXP_HOURS`
   - `GEMINI_API_KEY`
   - `GEMINI_MODEL`
5. Deploy.

## Security Notes

- Use a strong random `JWT_SECRET`.
- Never commit `.env` to GitHub.
- Passwords are salted/hashed with bcrypt.
- Keep Gemini and MongoDB credentials in environment secrets only.

## Module Coverage

- ✅ Auth (registration/login/logout/JWT/profile)
- ✅ Resume parsing (PDF/DOCX)
- ✅ ATS scoring (0-100 with metric breakdown)
- ✅ JD matching and skill gap detection
- ✅ Interview question generation (10/category)
- ✅ Mock interview answer evaluation
- ✅ Feedback report with strengths/weaknesses
- ✅ Analytics cards + Plotly trends
- ✅ Interview report viewing and CSV export
