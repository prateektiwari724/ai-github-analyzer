from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from github_utils import get_repo_data, get_readme, get_contributors
from nlp_summarizer import (
    detect_tech_stack,
    detect_project_type,
    detect_architecture,
    generate_summary,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/summarize/{owner}/{repo}")
def summarize(owner: str, repo: str):

    try:
        repo_data = get_repo_data(owner, repo)
        readme = get_readme(owner, repo)
        contributors = get_contributors(owner, repo)

        if not repo_data:
            return JSONResponse({"error": "Repo not found"}, status_code=404)

        language = repo_data.get("language", "Unknown")

        tech_stack = detect_tech_stack(readme or "", language)
        project_type = detect_project_type(readme or "")
        architecture = detect_architecture(project_type)

        summary = generate_summary(
            repo,
            project_type,
            language,
            tech_stack,
            readme or "",
        )

        return {
            "stars": repo_data.get("stars", 0),
            "forks": repo_data.get("forks", 0),
            "watchers": repo_data.get("watchers", 0),
            "open_issues": repo_data.get("open_issues", 0),
            "language": language,
            "license": repo_data.get("license", "Unknown"),
            "last_updated": repo_data.get("last_updated", "Unknown"),
            "size": repo_data.get("size", 0),
            "contributors": contributors,
            "tech_stack": ", ".join(tech_stack),
            "architecture": architecture,
            "project_type": project_type,
            "summary": summary,
        }

    except Exception as e:
        print("ERROR:", str(e))
        return JSONResponse({"error": "Internal Server Error"}, status_code=500)