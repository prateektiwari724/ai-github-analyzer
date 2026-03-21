import streamlit as st
import requests

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="GitHub Analyzer", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: #FAFAFA;
}

.title {
    text-align: center;
    font-size: 36px;
    font-weight: 600;
    margin-bottom: 20px;
}

.section-title {
    font-size: 22px;
    margin-top: 30px;
    margin-bottom: 15px;
    font-weight: 500;
}

.card {
    background-color: #111827;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #1F2937;
}

.metric-title {
    font-size: 16px;
    color: #9CA3AF;
}

.metric-value {
    font-size: 22px;
    font-weight: 600;
    margin-top: 8px;
}

.analysis-box {
    background-color: #1F2937;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ FUNCTIONS ------------------

def get_repo_data(url):
    try:
        parts = url.split("/")
        owner = parts[-2]
        repo = parts[-1]

        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        response = requests.get(api_url)

        if response.status_code != 200:
            return None

        return response.json()

    except:
        return None


def get_readme(owner, repo):
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"
    r = requests.get(url)

    if r.status_code == 200:
        return r.text
    return ""


def convert_size(size_kb):
    mb = size_kb / 1024
    return f"{mb:.2f} MB"


def detect_project_type(repo):
    topics = repo.get("topics", [])
    desc = (repo.get("description") or "").lower()

    if "api" in desc:
        return "API Service"
    if "web" in desc or "frontend" in desc:
        return "Web Application"
    if "cli" in desc:
        return "CLI Tool"
    if "ai" in desc or "ml" in desc:
        return "AI/ML Project"

    return "Software Project"


def detect_architecture(repo):
    desc = (repo.get("description") or "").lower()

    if "microservice" in desc:
        return "Microservices Architecture"
    if "api" in desc:
        return "Service-Based Architecture"
    if "cli" in desc:
        return "Command-line Architecture"

    return "General Architecture"


def generate_summary(repo, readme):
    name = repo.get("name", "")
    desc = repo.get("description", "")
    lang = repo.get("language", "")

    summary = f"{name} is a project"

    if lang:
        summary += f" built using {lang}"

    if desc:
        summary += f". {desc}"

    # add README first line if available
    if readme:
        first_line = readme.strip().split("\n")[0]
        if len(first_line) < 150:
            summary += f"\n\n{first_line}"

    return summary


# ------------------ UI ------------------

st.markdown('<div class="title">AI GitHub Repository Analyzer</div>', unsafe_allow_html=True)

repo_url = st.text_input("Enter GitHub Repository URL")

if st.button("Analyze"):

    with st.spinner("Analyzing repository..."):

        repo = get_repo_data(repo_url)

        if not repo:
            st.error("Invalid GitHub URL")
        else:
            owner = repo["owner"]["login"]
            repo_name = repo["name"]

            readme = get_readme(owner, repo_name)

            # ---------------- METRICS ----------------
            st.markdown('<div class="section-title">Repository Metrics</div>', unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)

            col1.markdown(f"""
            <div class="card">
                <div class="metric-title">Stars</div>
                <div class="metric-value">{repo.get("stargazers_count")}</div>
            </div>
            """, unsafe_allow_html=True)

            col2.markdown(f"""
            <div class="card">
                <div class="metric-title">Watchers</div>
                <div class="metric-value">{repo.get("subscribers_count")}</div>
            </div>
            """, unsafe_allow_html=True)

            col3.markdown(f"""
            <div class="card">
                <div class="metric-title">Issues</div>
                <div class="metric-value">{repo.get("open_issues_count")}</div>
            </div>
            """, unsafe_allow_html=True)

            col4.markdown(f"""
            <div class="card">
                <div class="metric-title">Language</div>
                <div class="metric-value">{repo.get("language")}</div>
            </div>
            """, unsafe_allow_html=True)

            # ---------------- DETAILS ----------------
            st.markdown('<div class="section-title">Details</div>', unsafe_allow_html=True)

            col5, col6 = st.columns(2)

            col5.markdown(f"""
            <div class="card">
                <div class="metric-title">Forks</div>
                <div class="metric-value">{repo.get("forks_count")}</div>
            </div>
            """, unsafe_allow_html=True)

            col6.markdown(f"""
            <div class="card">
                <div class="metric-title">Size</div>
                <div class="metric-value">{convert_size(repo.get("size"))}</div>
            </div>
            """, unsafe_allow_html=True)

            # ---------------- ANALYSIS ----------------
            st.markdown('<div class="section-title">Analysis</div>', unsafe_allow_html=True)

            project_type = detect_project_type(repo)
            architecture = detect_architecture(repo)
            tech_stack = repo.get("language")

            st.markdown(f'<div class="analysis-box"><b>Project Type:</b> {project_type}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="analysis-box"><b>Architecture:</b> {architecture}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="analysis-box"><b>Tech Stack:</b> {tech_stack}</div>', unsafe_allow_html=True)

            # ---------------- SUMMARY ----------------
            st.markdown('<div class="section-title">Summary</div>', unsafe_allow_html=True)

            summary = generate_summary(repo, readme)
            st.write(summary)