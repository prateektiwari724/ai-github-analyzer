import streamlit as st
import requests

st.set_page_config(page_title="AI GitHub Analyzer", layout="wide")

# ---------- FUNCTIONS ----------

def get_repo_data(repo_url):
    repo_path = repo_url.replace("https://github.com/", "")
    api_url = f"https://api.github.com/repos/{repo_path}"
    readme_url = f"https://api.github.com/repos/{repo_path}/readme"

    repo_data = requests.get(api_url).json()

    readme = ""
    try:
        readme_data = requests.get(readme_url).json()
        import base64
        readme = base64.b64decode(readme_data["content"]).decode("utf-8")
    except:
        pass

    return repo_data, readme


def detect_project_type(readme, description):
    text = (readme + " " + str(description)).lower()

    if any(x in text for x in ["react", "next.js", "frontend", "ui"]):
        return "Frontend Web App", "Component-Based Architecture"

    elif any(x in text for x in ["api", "backend", "server"]):
        return "Backend API", "REST API Architecture"

    elif any(x in text for x in ["machine learning", "model", "ai"]):
        return "AI/ML Project", "Model-based Architecture"

    elif any(x in text for x in ["cli", "command line"]):
        return "CLI Tool", "Command-line Architecture"

    else:
        return "Software Project", "General Software Architecture"


def generate_summary(name, description, readme, language):
    return f"""
{name} is a project developed using {language}.

{description if description else "No description available."}

Key Insights:
- Uses {language}
- Based on repository structure and documentation

Strength:
- Structured and practical project

Limitation:
- Analysis based on public metadata (no deep code scan)
"""


# ---------- UI ----------

st.title("🚀 AI GitHub Repository Analyzer")

repo_url = st.text_input("🔗 Enter GitHub Repo URL")

if st.button("Analyze"):

    repo, readme = get_repo_data(repo_url)

    if not repo or "message" in repo:
        st.error("Invalid GitHub URL")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📊 Repository Metrics")
            st.metric("⭐ Stars", repo["stargazers_count"])
            st.metric("👁 Watchers", repo["watchers_count"])
            st.metric("🐞 Issues", repo["open_issues_count"])
            st.metric("💻 Language", repo["language"])

        with col2:
            st.markdown("### 📦 Details")
            st.metric("🍴 Forks", repo["forks_count"])
            st.metric("📏 Size", repo["size"])
            st.write("🕒 Updated:", repo["updated_at"])
            st.write("👥 Contributors: N/A")

        # ---------- Analysis ----------
        project_type, architecture = detect_project_type(
            readme,
            repo.get("description")
        )

        st.markdown("## 🧠 Analysis")

        col3, col4 = st.columns(2)

        with col3:
            st.info(f"**Project Type:** {project_type}")
            st.info(f"**Architecture:** {architecture}")

        with col4:
            st.success(f"**Tech Stack:** {repo.get('language')}")

        # ---------- Summary ----------
        st.markdown("## 📄 Summary")

        summary = generate_summary(
            repo.get("name"),
            repo.get("description"),
            readme,
            repo.get("language")
        )

        st.write(summary)