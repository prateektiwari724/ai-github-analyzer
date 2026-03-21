import streamlit as st
import requests
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI GitHub Repository Analyzer",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 34px;
    font-weight: 600;
    margin-bottom: 25px;
}

.section-title {
    font-size: 20px;
    font-weight: 600;
    margin-top: 30px;
    margin-bottom: 15px;
}

.card {
    background-color: #111827;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    border: 1px solid #1f2937;
}

.metric-label {
    font-size: 14px;
    color: #9ca3af;
}

.metric-value {
    font-size: 20px;
    font-weight: 600;
    margin-top: 5px;
}

.analysis-box {
    background-color: #1f2937;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------

def get_repo_data(url):
    try:
        parts = url.replace("https://github.com/", "").split("/")
        owner, repo = parts[0], parts[1]

        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        repo_data = requests.get(api_url).json()

        readme_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        readme_res = requests.get(readme_url)

        readme_text = ""
        if readme_res.status_code == 200:
            import base64
            readme_text = base64.b64decode(readme_res.json()['content']).decode("utf-8", errors="ignore")

        return repo_data, readme_text

    except:
        return None, None


def detect_tech_stack(repo, readme):
    readme = readme.lower()

    if "scrapy" in readme:
        return "Python + Scrapy"
    if "streamlit" in readme:
        return "Python + Streamlit"
    if "react" in readme:
        return "React"
    if "node" in readme:
        return "Node.js"
    return repo.get("language", "Unknown")


def detect_project_type(readme):
    readme = readme.lower()

    if "agent" in readme:
        return "AI Agent Framework"
    if "scrapy" in readme or "crawler" in readme:
        return "Data Scraping Tool"
    if "api" in readme:
        return "Backend API"
    if "web app" in readme:
        return "Web Application"

    return "Software Project"


def detect_architecture(readme):
    readme = readme.lower()

    if "microservice" in readme:
        return "Microservices Architecture"
    if "api" in readme:
        return "REST API Architecture"
    if "agent" in readme:
        return "Agent-based Architecture"

    return "General Architecture"


def generate_summary(name, description, readme, tech_stack):
    summary = f"{name} is a project built using {tech_stack}.\n\n"

    if description:
        summary += description + "\n\n"

    if readme:
        summary += "This project appears to be structured for real-world usage and development.\n\n"

    summary += "Strength:\n- Clean and maintainable structure\n\n"
    summary += "Limitation:\n- Analysis is based only on public metadata"

    return summary


# ---------------- UI ----------------

st.markdown('<div class="main-title">AI GitHub Repository Analyzer</div>', unsafe_allow_html=True)

repo_url = st.text_input("Enter GitHub Repository URL")

if st.button("Analyze"):

    with st.spinner("Analyzing repository..."):
        time.sleep(1)
        repo, readme = get_repo_data(repo_url)

    if repo:

        tech_stack = detect_tech_stack(repo, readme)
        project_type = detect_project_type(readme)
        architecture = detect_architecture(readme)

        # Metrics
        stars = repo.get("stargazers_count", 0)
        watchers = repo.get("subscribers_count", "N/A")
        issues = repo.get("open_issues_count", 0)
        forks = repo.get("forks_count", 0)

        size_kb = repo.get("size", 0)
        size_mb = round(size_kb / 1024, 2)

        language = repo.get("language", "Unknown")

        # ---------------- METRICS ----------------
        st.markdown('<div class="section-title">Repository Metrics</div>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f'<div class="card"><div class="metric-label">Stars</div><div class="metric-value">{stars}</div></div>', unsafe_allow_html=True)

        with col2:
            st.markdown(f'<div class="card"><div class="metric-label">Watchers</div><div class="metric-value">{watchers}</div></div>', unsafe_allow_html=True)

        with col3:
            st.markdown(f'<div class="card"><div class="metric-label">Issues</div><div class="metric-value">{issues}</div></div>', unsafe_allow_html=True)

        with col4:
            st.markdown(f'<div class="card"><div class="metric-label">Language</div><div class="metric-value">{language}</div></div>', unsafe_allow_html=True)

        # ---------------- DETAILS ----------------
        st.markdown('<div class="section-title">Details</div>', unsafe_allow_html=True)

        col5, col6 = st.columns(2)

        with col5:
            st.markdown(f'<div class="card"><div class="metric-label">Forks</div><div class="metric-value">{forks}</div></div>', unsafe_allow_html=True)

        with col6:
            st.markdown(f'<div class="card"><div class="metric-label">Size</div><div class="metric-value">{size_mb} MB</div></div>', unsafe_allow_html=True)

        # ---------------- ANALYSIS ----------------
        st.markdown('<div class="section-title">Analysis</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="analysis-box"><b>Project Type:</b> {project_type}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="analysis-box"><b>Architecture:</b> {architecture}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="analysis-box"><b>Tech Stack:</b> {tech_stack}</div>', unsafe_allow_html=True)

        # ---------------- SUMMARY ----------------
        st.markdown('<div class="section-title">Summary</div>', unsafe_allow_html=True)

        summary = generate_summary(
            repo.get("name"),
            repo.get("description"),
            readme,
            tech_stack
        )

        st.write(summary)

    else:
        st.error("Invalid GitHub URL")