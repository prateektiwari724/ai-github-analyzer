import streamlit as st
import requests
import base64
import time

st.set_page_config(page_title="GitHub Analyzer", layout="wide")

# ---------- FUNCTIONS ----------

def fetch_data(repo_url):
    repo_path = repo_url.replace("https://github.com/", "")
    repo_api = f"https://api.github.com/repos/{repo_path}"
    readme_api = f"https://api.github.com/repos/{repo_path}/readme"

    repo = requests.get(repo_api).json()

    readme = ""
    try:
        r = requests.get(readme_api).json()
        readme = base64.b64decode(r["content"]).decode("utf-8")
    except:
        pass

    return repo, readme


def detect_type(readme, description):
    text = (readme + " " + str(description)).lower()

    if any(x in text for x in ["langchain", "agent", "llm", "rag"]):
        return "AI Framework", "Agent-based Architecture"

    elif any(x in text for x in ["react", "next", "frontend"]):
        return "Frontend Web App", "Component-Based Architecture"

    elif any(x in text for x in ["api", "backend"]):
        return "Backend API", "REST Architecture"

    elif any(x in text for x in ["cli", "command line"]):
        return "CLI Tool", "Command-line Architecture"

    return "Software Project", "General Architecture"


def generate_summary(name, desc, readme, lang):
    base = desc if desc else "No description available."

    return f"""
{name} is a project built using {lang}.

{base}

This project appears to be structured for real-world usage and scalability.

Strength:
- Clean and maintainable structure

Limitation:
- Analysis is based only on public metadata
"""


# ---------- CUSTOM CSS ----------

st.markdown("""
<style>
body {
    font-family: 'Inter', sans-serif;
}

/* Title */
.main-title {
    text-align: center;
    font-size: 32px;
    font-weight: 600;
    margin-bottom: 25px;
}

/* Input */
.stTextInput > div > div > input {
    padding: 10px;
}

/* Cards */
.card {
    background-color: #111827;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #1f2937;
}

/* Metric title */
.metric-title {
    font-size: 16px;
    color: #9ca3af;
    margin-bottom: 5px;
}

/* Metric value */
.metric-value {
    font-size: 20px;
    font-weight: 600;
}

/* Section headings */
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-top: 30px;
    margin-bottom: 15px;
}

/* Analysis box */
.analysis-box {
    background-color: #1f2937;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- UI ----------

st.markdown('<div class="main-title">AI GitHub Repository Analyzer</div>', unsafe_allow_html=True)

repo_url = st.text_input("Enter GitHub Repository URL")

if st.button("Analyze"):

    with st.spinner("Analyzing repository..."):
        time.sleep(1.2)

        repo, readme = fetch_data(repo_url)

        if "message" in repo:
            st.error("Invalid repository URL")
        else:

            # ---------- METRICS GRID ----------
            st.markdown('<div class="section-title">Repository Metrics</div>', unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="card">
                    <div class="metric-title">Stars</div>
                    <div class="metric-value">{repo["stargazers_count"]}</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="card">
                    <div class="metric-title">Watchers</div>
                    <div class="metric-value">{repo["watchers_count"]}</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="card">
                    <div class="metric-title">Issues</div>
                    <div class="metric-value">{repo["open_issues_count"]}</div>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                <div class="card">
                    <div class="metric-title">Language</div>
                    <div class="metric-value">{repo["language"]}</div>
                </div>
                """, unsafe_allow_html=True)

            # ---------- DETAILS ----------
            st.markdown('<div class="section-title">Details</div>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"""
                <div class="card">
                    <div class="metric-title">Forks</div>
                    <div class="metric-value">{repo["forks_count"]}</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="card">
                    <div class="metric-title">Size</div>
                    <div class="metric-value">{repo["size"]}</div>
                </div>
                """, unsafe_allow_html=True)

            # ---------- ANALYSIS ----------
            ptype, arch = detect_type(readme, repo.get("description"))

            st.markdown('<div class="section-title">Analysis</div>', unsafe_allow_html=True)

            st.markdown(f"""
            <div class="analysis-box"><b>Project Type:</b> {ptype}</div>
            <div class="analysis-box"><b>Architecture:</b> {arch}</div>
            <div class="analysis-box"><b>Tech Stack:</b> {repo.get("language")}</div>
            """, unsafe_allow_html=True)

            # ---------- SUMMARY ----------
            st.markdown('<div class="section-title">Summary</div>', unsafe_allow_html=True)

            st.write(generate_summary(
                repo.get("name"),
                repo.get("description"),
                readme,
                repo.get("language")
            ))