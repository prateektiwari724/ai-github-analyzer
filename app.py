import streamlit as st
import requests

st.set_page_config(page_title="AI GitHub Analyzer", layout="wide")

# ---------- FUNCTIONS ----------

def get_repo_data(repo_url):
    try:
        repo_path = repo_url.replace("https://github.com/", "")
        api_url = f"https://api.github.com/repos/{repo_path}"

        response = requests.get(api_url)
        data = response.json()

        return data
    except:
        return None


def detect_project_type(readme, language):
    text = (readme or "").lower()

    if "api" in text:
        return "Backend API", "REST API Architecture"
    elif "react" in text or "frontend" in text:
        return "Frontend Web App", "Component-Based Architecture"
    elif "machine learning" in text or "model" in text:
        return "ML Project", "Model-based Architecture"
    elif "cli" in text:
        return "CLI Tool", "Command-line Architecture"
    else:
        return "Software Project", "General Software Architecture"


def generate_summary(name, description, language):
    return f"""
{name} is a project developed using {language}.

{description if description else "No description available."}

This project appears to be structured for practical use and development.

Strength:
- Uses {language} ecosystem

Limitation:
- Limited context from repository metadata
"""


# ---------- UI ----------

st.title("🚀 AI GitHub Repository Analyzer")

repo_url = st.text_input("Enter GitHub Repo URL")

if st.button("Analyze"):

    data = get_repo_data(repo_url)

    if not data or "message" in data:
        st.error("Invalid GitHub URL")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Repository Metrics")
            st.write("⭐ Stars:", data.get("stargazers_count"))
            st.write("👁 Watchers:", data.get("watchers_count"))
            st.write("🐞 Issues:", data.get("open_issues_count"))
            st.write("💻 Language:", data.get("language"))

        with col2:
            st.subheader("📦 Details")
            st.write("🍴 Forks:", data.get("forks_count"))
            st.write("📏 Size:", data.get("size"))
            st.write("🕒 Updated:", data.get("updated_at"))
            st.write("👥 Contributors:", "N/A")

        # Analysis
        project_type, architecture = detect_project_type(
            data.get("description"),
            data.get("language")
        )

        st.subheader("🧠 Analysis")
        st.write("**Project Type:**", project_type)
        st.write("**Architecture:**", architecture)
        st.write("**Tech Stack:**", data.get("language"))

        # Summary
        st.subheader("📄 Summary")

        summary = generate_summary(
            data.get("name"),
            data.get("description"),
            data.get("language")
        )

        st.write(summary)