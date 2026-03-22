import streamlit as st
from github_utils import extract_repo_info, get_readme
from nlp_summarizer import summarize_text

st.set_page_config(page_title="AI GitHub Analyzer", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 36px;
    font-weight: 600;
    margin-bottom: 20px;
}

.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-top: 30px;
}

.card {
    background-color: #111827;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    border: 1px solid #1f2937;
}

.metric-title {
    font-size: 16px;
    color: #9ca3af;
}

.metric-value {
    font-size: 22px;
    font-weight: 600;
    margin-top: 5px;
}

.summary-box {
    background-color: #111827;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #1f2937;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown('<div class="main-title">AI GitHub Repository Analyzer</div>', unsafe_allow_html=True)

# ---------- INPUT ----------
repo_url = st.text_input("Enter GitHub Repository URL")

if st.button("Analyze"):
    with st.spinner("Analyzing repository..."):
        repo = extract_repo_info(repo_url)

        if not repo:
            st.error("Invalid repository URL")
        else:
            readme = get_readme(repo_url)
            summary = summarize_text(readme)

            # ---------- METRICS ----------
            st.markdown('<div class="section-title">Repository Metrics</div>', unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)

            def card(title, value):
                return f"""
                <div class="card">
                    <div class="metric-title">{title}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """

            col1.markdown(card("Stars", repo["stars"]), unsafe_allow_html=True)
            col2.markdown(card("Watchers", repo["watchers"]), unsafe_allow_html=True)
            col3.markdown(card("Issues", repo["issues"]), unsafe_allow_html=True)
            col4.markdown(card("Language", repo["language"]), unsafe_allow_html=True)

            # ---------- DETAILS ----------
            st.markdown('<div class="section-title">Details</div>', unsafe_allow_html=True)

            col5, col6 = st.columns(2)
            col5.markdown(card("Forks", repo["forks"]), unsafe_allow_html=True)
            col6.markdown(card("Size", f"{repo['size']} MB"), unsafe_allow_html=True)

            # ---------- ANALYSIS ----------
            st.markdown('<div class="section-title">Analysis</div>', unsafe_allow_html=True)

            st.markdown(f"""
            <div class="card">Project Type: {"AI/ML Project" if "AI" in (repo["description"] or "") else "Software Project"}</div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="card">Tech Stack: {repo["language"]}</div>
            """, unsafe_allow_html=True)

            # ---------- SUMMARY ----------
            st.markdown('<div class="section-title">Summary (NLP Based)</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)