import streamlit as st
import requests

st.set_page_config(page_title="AI GitHub Analyzer", layout="centered")

st.title("🚀 AI GitHub Repository Analyzer")

repo_url = st.text_input("Enter GitHub Repository URL")

if st.button("Analyze"):

    if not repo_url:
        st.warning("Please enter a GitHub URL")
    else:
        try:
            parts = repo_url.strip().split("/")
            owner = parts[3]
            repo = parts[4]

            # GitHub API
            repo_api = f"https://api.github.com/repos/{owner}/{repo}"
            data = requests.get(repo_api).json()

            # Contributors
            contributors_api = f"{repo_api}/contributors"
            contributors = requests.get(contributors_api).json()

            st.subheader("📊 Repository Metrics")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("⭐ Stars", data.get("stargazers_count", 0))
                st.metric("👀 Watchers", data.get("watchers_count", 0))
                st.metric("📝 Open Issues", data.get("open_issues_count", 0))
                st.metric("💻 Language", data.get("language", "N/A"))

            with col2:
                st.metric("🍴 Forks", data.get("forks_count", 0))
                st.metric("📦 Size", data.get("size", 0))
                st.metric("📅 Updated", data.get("updated_at", "N/A"))
                st.metric("👥 Contributors", len(contributors))

            # Tech Stack (simple logic)
            tech_stack = data.get("language", "Unknown")

            # Project Type logic
            if "web" in repo.lower():
                project_type = "Web Application"
                architecture = "Frontend Web Architecture"
            elif "api" in repo.lower():
                project_type = "Backend API"
                architecture = "REST API Architecture"
            else:
                project_type = "Software Project"
                architecture = "General Software Architecture"

            st.subheader("🧠 Analysis")

            st.write(f"**Project Type:** {project_type}")
            st.write(f"**Architecture:** {architecture}")
            st.write(f"**Tech Stack:** {tech_stack}")

            st.subheader("📄 Summary")

            description = data.get("description", "No description available")

            summary = f"""
{repo} is a {project_type} developed using {tech_stack}.

It focuses on solving real-world problems and improving developer productivity.

Strength: Well-structured and practical.

Limitation: May require setup and learning effort.
"""

            st.write(summary)

        except:
            st.error("Invalid GitHub URL or API error")