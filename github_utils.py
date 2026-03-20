import requests

BASE_URL = "https://api.github.com/repos"


def get_repo_data(owner, repo):
    url = f"{BASE_URL}/{owner}/{repo}"
    res = requests.get(url)

    if res.status_code != 200:
        return None

    data = res.json()

    return {
        "stars": data.get("stargazers_count"),
        "forks": data.get("forks_count"),
        "watchers": data.get("watchers_count"),
        "open_issues": data.get("open_issues_count"),
        "language": data.get("language"),
        "license": data.get("license", {}).get("name") if data.get("license") else "None",
        "last_updated": data.get("updated_at"),
        "size": data.get("size"),
    }


def get_readme(owner, repo):
    url = f"{BASE_URL}/{owner}/{repo}/readme"
    headers = {"Accept": "application/vnd.github.v3.raw"}

    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        return res.text

    return ""


def get_contributors(owner, repo):
    url = f"{BASE_URL}/{owner}/{repo}/contributors"
    res = requests.get(url)

    if res.status_code != 200:
        return 0

    return len(res.json())