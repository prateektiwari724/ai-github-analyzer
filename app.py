import streamlit as st
from github_utils import get_repo_data, get_readme
from nlp_summarizer import summarize_text
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI GitHub Analyzer", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}

/* Center Title */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #e5e7eb;
    margin-bottom: 30px;
}

/* Input */
.stTextInput>div>div>input {
    background-color: #1f2937;
    color: white;
    border-radius: 10px;
}

/* Button */
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    padding: 8px 20px;
}

/* Cards */
.metric-card {
    background-color: #111827;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    transition: 0.3s;
}

.metric-card:hover {
    transform: scale(1.03);
}

/* Metric title */
.metric-title {
    font-size: 16px;
    color: #9ca3af;
    margin-bottom: 10px;
}

/* Metric value */
.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: #f9fafb;
}

/* Section titles */
.section-title {
    font-size: 26px;
    font-weight: bold;
    margin-top: 40px;
    margin-bottom: 15px;
    color: #e5e7eb;
}

/* Summary box */
.summary-box {
    background-color: #111827;
    padding: 20px;
    border-radius: 12px;
    line-height: 1.7;
    color: #e5e7eb;
    font-size: 15px;
}

/* Loader */
.loader {
  border: 6px solid #1f2937;
  border-top: 6px solid #2563eb;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: auto;
}

@keyframes spin {
  0% { transform: rotate(0deg);}
  100% { transform: rotate(360deg);}
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="title">AI GitHub Repository Analyzer</div>', unsafe_allow_html=True)

# ---------------- INPUT ----------------
repo_url = st.text_input("Enter GitHub Repository URL")

if st.button("Analyze"):

    if not repo_url:
        st.warning("Please enter a GitHub URL")

    else:
        try:
            # -------- LOADING --------
            loader = st.empty()
            loader.markdown('<div class="loader"></div>', unsafe_allow_html=True)
            time.sleep(1)

            # -------- FETCH DATA --------
            data = get_repo_data(repo_url)
            readme = get_readme(repo_url)

            summary = summarize_text(readme)

            loader.empty()

            # -------- METRICS --------
            st.markdown('<div class="section-title">Repository Metrics</div>', unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Stars</div>
                    <div class="metric-value">{data['stars']}</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Watchers</div>
                    <div class="metric-value">{data['watchers']}</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Issues</div>
                    <div class="metric-value">{data['issues']}</div>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Language</div>
                    <div class="metric-value">{data['language']}</div>
                </div>
                """, unsafe_allow_html=True)

            col5, col6 = st.columns(2)

            with col5:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Forks</div>
                    <div class="metric-value">{data['forks']}</div>
                </div>
                """, unsafe_allow_html=True)

            with col6:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Size</div>
                    <div class="metric-value">{round(data['size'], 2)} MB</div>
                </div>
                """, unsafe_allow_html=True)

            # -------- ANALYSIS --------
            st.markdown('<div class="section-title">Analysis</div>', unsafe_allow_html=True)

            readme_lower = readme.lower() if readme else ""

            project_type = "Web Application" if "web" in readme_lower else "Software Project"
            architecture = "Modular Architecture" if any(x in readme_lower for x in ["api", "service", "microservice"]) else "General Architecture"
            tech_stack = data.get("language", "Unknown")

            st.write(f"Project Type: {project_type}")
            st.write(f"Architecture: {architecture}")
            st.write(f"Tech Stack: {tech_stack}")

            # -------- SUMMARY --------
            st.markdown('<div class="section-title">Project Summary</div>', unsafe_allow_html=True)

            # Safety fallback
            if not summary or summary.strip() == "":
                summary = """
Overview:
This repository contains a software project hosted on GitHub.

Key Features:
- Provides core functionality.
- Designed for specific use cases.

Purpose:
Demonstrates implementation and development practices.

Additional Info:
Refer to repository documentation for more details.
"""

            st.markdown(f"""
            <div class="summary-box">
            {summary.replace("\n", "<br>")}
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {str(e)import streamlit as st
from github_utils import get_repo_data, get_readme
from nlp_summarizer import summarize_text
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI GitHub Analyzer", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}

/* Center Title */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #e5e7eb;
    margin-bottom: 30px;
}

/* Input */
.stTextInput>div>div>input {
    background-color: #1f2937;
    color: white;
    border-radius: 10px;
}

/* Button */
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    padding: 8px 20px;
}

/* Cards */
.metric-card {
    background-color: #111827;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    transition: 0.3s;
}

.metric-card:hover {
    transform: scale(1.03);
}

/* Metric title */
.metric-title {
    font-size: 16px;
    color: #9ca3af;
    margin-bottom: 10px;
}

/* Metric value */
.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: #f9fafb;
}

/* Section titles */
.section-title {
    font-size: 26px;
    font-weight: bold;
    margin-top: 40px;
    margin-bottom: 15px;
    color: #e5e7eb;
}

/* Summary box */
.summary-box {
    background-color: #111827;
    padding: 20px;
    border-radius: 12px;
    line-height: 1.7;
    color: #e5e7eb;
    font-size: 15px;
}

/* Loader */
.loader {
  border: 6px solid #1f2937;
  border-top: 6px solid #2563eb;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: auto;
}

@keyframes spin {
  0% { transform: rotate(0deg);}
  100% { transform: rotate(360deg);}
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="title">AI GitHub Repository Analyzer</div>', unsafe_allow_html=True)

# ---------------- INPUT ----------------
repo_url = st.text_input("Enter GitHub Repository URL")

if st.button("Analyze"):

    if not repo_url:
        st.warning("Please enter a GitHub URL")

    else:
        try:
            # -------- LOADING --------
            loader = st.empty()
            loader.markdown('<div class="loader"></div>', unsafe_allow_html=True)
            time.sleep(1)

            # -------- FETCH DATA --------
            data = get_repo_data(repo_url)
            readme = get_readme(repo_url)

            summary = summarize_text(readme)

            loader.empty()

            # -------- METRICS --------
            st.markdown('<div class="section-title">Repository Metrics</div>', unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Stars</div>
                    <div class="metric-value">{data['stars']}</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Watchers</div>
                    <div class="metric-value">{data['watchers']}</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Issues</div>
                    <div class="metric-value">{data['issues']}</div>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Language</div>
                    <div class="metric-value">{data['language']}</div>
                </div>
                """, unsafe_allow_html=True)

            col5, col6 = st.columns(2)

            with col5:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Forks</div>
                    <div class="metric-value">{data['forks']}</div>
                </div>
                """, unsafe_allow_html=True)

            with col6:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Size</div>
                    <div class="metric-value">{round(data['size'], 2)} MB</div>
                </div>
                """, unsafe_allow_html=True)

            # -------- ANALYSIS --------
            st.markdown('<div class="section-title">Analysis</div>', unsafe_allow_html=True)

            readme_lower = readme.lower() if readme else ""

            project_type = "Web Application" if "web" in readme_lower else "Software Project"
            architecture = "Modular Architecture" if any(x in readme_lower for x in ["api", "service", "microservice"]) else "General Architecture"
            tech_stack = data.get("language", "Unknown")

            st.write(f"Project Type: {project_type}")
            st.write(f"Architecture: {architecture}")
            st.write(f"Tech Stack: {tech_stack}")

            # -------- SUMMARY --------
            st.markdown('<div class="section-title">Project Summary</div>', unsafe_allow_html=True)

            # Safety fallback
            if not summary or summary.strip() == "":
                summary = """
Overview:
This repository contains a software project hosted on GitHub.

Key Features:
- Provides core functionality.
- Designed for specific use cases.

Purpose:
Demonstrates implementation and development practices.

Additional Info:
Refer to repository documentation for more details.
"""

            st.markdown(f"""
            <div class="summary-box">
            {summary.replace("\n", "<br>")}
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {str(e)}")