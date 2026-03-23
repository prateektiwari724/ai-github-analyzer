import streamlit as st
import requests
import re
import time
from nlp_summarizer import summarize_text

st.set_page_config(page_title="AI GitHub Repository Analyzer", layout="wide")

# ---------------- UI ----------------
st.markdown("""
<style>
.big-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}
.metric-card {
    background: #111827;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    width: 100%;
}
.metric-title { color: #9CA3AF; }
.metric-value { font-size: 26px; font-weight: bold; }
.summary-box {
    background: #111827;
    padding: 20px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">AI GitHub Repository Analyzer</div>', unsafe_allow_html=True)

repo_url = st.text_input("Enter GitHub Repository URL")

# ---------------- FUNCTIONS ----------------

def extract_repo(url):
    match = re.search(r"github\.com/([^/]+)/([^/]+)", url)
    return match.group(1), match.group(2) if match else (None, None)


def get_repo(owner, repo):
    return requests.get(f"https://api.github.com/repos/{owner}/{repo}").json()


def get_readme(owner, repo):
    urls = [
        f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md",
        f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md"
    ]

    for url in urls:
        r = requests.get(url)
        if r.status_code == 200:
            return r.text

    return ""

# ---------------- BUTTON ----------------

if st.button("Analyze"):

    if not repo_url:
        st.warning("Enter URL")
    else:
        owner, repo = extract_repo(repo_url)

        if not owner:
            st.error("Invalid URL")
        else:
            try:
                with st.spinner("Analyzing repository..."):
                    time.sleep(1)

                    data = get_repo(owner, repo)
                    readme = get_readme(owner, repo)
                    summary = summarize_text(readme)

                # ---------- METRICS ----------
                st.subheader("Repository Metrics")

                c1, c2, c3, c4 = st.columns(4)

                c1.markdown(f"<div class='metric-card'><div class='metric-title'>Stars</div><div class='metric-value'>{data.get('stargazers_count',0)}</div></div>", unsafe_allow_html=True)
                c2.markdown(f"<div class='metric-card'><div class='metric-title'>Watchers</div><div class='metric-value'>{data.get('watchers_count',0)}</div></div>", unsafe_allow_html=True)
                c3.markdown(f"<div class='metric-card'><div class='metric-title'>Issues</div><div class='metric-value'>{data.get('open_issues_count',0)}</div></div>", unsafe_allow_html=True)
                c4.markdown(f"<div class='metric-card'><div class='metric-title'>Language</div><div class='metric-value'>{data.get('language','N/A')}</div></div>", unsafe_allow_html=True)

                # ✅ FIX: Proper spacing row (prevents overlap)
                st.markdown("<br>", unsafe_allow_html=True)

                # ✅ FIXED ROW (equal width, no overlap)
                c5, c6 = st.columns([1, 1])

                c5.markdown(f"<div class='metric-card'><div class='metric-title'>Forks</div><div class='metric-value'>{data.get('forks_count',0)}</div></div>", unsafe_allow_html=True)
                c6.markdown(f"<div class='metric-card'><div class='metric-title'>Size</div><div class='metric-value'>{round(data.get('size',0)/1024,2)} MB</div></div>", unsafe_allow_html=True)

                # ---------- ANALYSIS ----------
                st.subheader("Analysis")
                st.write("Project Type: Software Project")
                st.write("Architecture: Modular Architecture")
                st.write(f"Tech Stack: {data.get('language','Unknown')}")

                # ---------- SUMMARY ----------
                st.subheader("Project Summary")

                st.markdown(f"""
                <div class="summary-box">

                <b>Overview:</b><br>
                {summary['overview']}<br><br>

                <b>Key Features:</b>
                <ul>
                {''.join([f"<li>{f}</li>" for f in summary['features']])}
                </ul>

                <b>Purpose:</b><br>
                {summary['purpose']}<br><br>

                <b>Additional Info:</b><br>
                {summary['additional']}

                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {str(e)}")