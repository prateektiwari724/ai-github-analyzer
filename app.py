import streamlit as st
from github_utils import get_repo_data, get_readme
from nlp_summarizer import clean_readme, summarize_text
import time

st.set_page_config(page_title="GitHub Analyzer", layout="wide")

# ---------- CSS ----------
st.markdown("""
<style>

/* Center Title */
h1 {
    text-align: center;
    font-size: 42px !important;
    margin-bottom: 30px;
}

/* Input */
input {
    transition: all 0.3s ease;
}
input:focus {
    border: 2px solid #6366F1 !important;
    box-shadow: 0 0 10px rgba(99,102,241,0.5);
}

/* Button */
button {
    transition: 0.3s;
}
button:hover {
    transform: scale(1.05);
}

/* Section Title */
.section-title {
    font-size: 26px;
    margin-top: 40px;
    margin-bottom: 15px;
    font-weight: 600;
}

/* Metric Cards */
.metric-card {
    background: #0f172a;
    padding: 30px;
    border-radius: 14px;
    text-align: center;
    transition: 0.3s;
    border: 1px solid #1e293b;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 20px rgba(99,102,241,0.4);
}

.metric-title {
    font-size: 16px;
    color: #94a3b8;
}

.metric-value {
    font-size: 30px;
    font-weight: 700;
    margin-top: 8px;
}

/* Summary */
.summary-box {
    background: #0f172a;
    padding: 25px;
    border-radius: 12px;
    line-height: 1.8;
    font-size: 16px;
    border: 1px solid #1e293b;
}

</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("AI GitHub Repository Analyzer")

repo_url = st.text_input("Enter GitHub Repository URL")

# ---------- BUTTON ----------
if st.button("Analyze"):

    if repo_url:

        # 🔥 LOADING ANIMATION
        with st.spinner("Analyzing repository..."):
            time.sleep(1)  # smooth UX
            repo = get_repo_data(repo_url)
            readme = get_readme(repo_url)

            clean_text = clean_readme(readme)
            summary = summarize_text(clean_text)

        # ---------- METRICS ----------
        st.markdown('<div class="section-title">Repository Metrics</div>', unsafe_allow_html=True)

        cols = st.columns(4)

        def card(title, value):
            return f"""
            <div class="metric-card">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """

        cols[0].markdown(card("Stars", repo.get("stars", 0)), unsafe_allow_html=True)
        cols[1].markdown(card("Watchers", repo.get("watchers", 0)), unsafe_allow_html=True)
        cols[2].markdown(card("Issues", repo.get("issues", 0)), unsafe_allow_html=True)
        cols[3].markdown(card("Language", repo.get("language", "N/A")), unsafe_allow_html=True)

        col5, col6 = st.columns(2)
        col5.markdown(card("Forks", repo.get("forks", 0)), unsafe_allow_html=True)
        col6.markdown(card("Size", repo.get("size", "N/A")), unsafe_allow_html=True)

        # ---------- ANALYSIS ----------
        st.markdown('<div class="section-title">Analysis</div>', unsafe_allow_html=True)

        project_type = "Web Application" if "web" in clean_text.lower() else "Software Project"
        architecture = "Modular Architecture" if "api" in clean_text.lower() else "General Architecture"

        st.write(f"Project Type: {project_type}")
        st.write(f"Architecture: {architecture}")
        st.write(f"Tech Stack: {repo.get('language', 'N/A')}")

        # ---------- SUMMARY ----------
        st.markdown('<div class="section-title">Project Summary</div>', unsafe_allow_html=True)

        st.markdown(f"<div class='summary-box'>{summary}</div>", unsafe_allow_html=True)

    else:
        st.warning("Enter a valid GitHub URL")