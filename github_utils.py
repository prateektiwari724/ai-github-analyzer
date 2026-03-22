import requests

def get_repo_data(url):
    try:
        parts = url.rstrip("/").split("/")
        owner = parts[-2]
        repo = parts[-1]

        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        res = requests.get(api_url).json()

        return {
            "stars": res.get("stargazers_count", 0),
            "watchers": res.get("watchers_count", 0),
            "issues": res.get("open_issues_count", 0),
            "language": res.get("language", "N/A"),
            "forks": res.get("forks_count", 0),
            "size": f"{round(res.get('size', 0)/1024,2)} MB"
        }

    except:
        return {}

def get_readme(url):
    try:
        parts = url.rstrip("/").split("/")
        owner = parts[-2]
        repo = parts[-1]

        api_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"
        res = requests.get(api_url)

        if res.status_code == 200:
            return res.text
        return ""

    except:
        return ""