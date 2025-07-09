import os
import sys
import json
import requests
from datetime import datetime
from urllib.parse import urlparse

# -------------------------------------------------------------------------
# GitHub Repo Metadata & Activity Scraper
#
# Usage: python scrape_github.py <github_repo_url>
# Requires optional GITHUB_TOKEN for higher rate limits and private repos.
# Fetches repo metadata, commit history, full issues & PR details, and appends to repos_metadata.json.
# -------------------------------------------------------------------------

# Parse owner and repo from URL
def parse_github_url(repo_url):
    parsed = urlparse(repo_url)
    parts = parsed.path.strip("/").split("/")
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL: use https://github.com/owner/repo")
    return parts[0], parts[1]

# Fetch repository metadata
def fetch_repo_metadata(owner, repo, headers):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    metadata = {
        "full_name": data.get("full_name"),
        "description": data.get("description"),
        "html_url": data.get("html_url"),
        "clone_url": data.get("clone_url"),
        "private": data.get("private"),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
        "pushed_at": data.get("pushed_at"),
        "stars": data.get("stargazers_count"),
        "forks": data.get("forks_count"),
        "watchers": data.get("subscribers_count"),
        "language": data.get("language"),
        "license": (data.get("license") or {}).get("name"),
        "owner": data.get("owner", {}).get("login"),
        "topics": [],
        "commits": [],
        "issues": [],
        "prs": []
    }

    # Fetch topics
    topics_url = f"https://api.github.com/repos/{owner}/{repo}/topics"
    resp = requests.get(topics_url, headers={**headers, "Accept": "application/vnd.github.mercy-preview+json"})
    if resp.ok:
        metadata["topics"] = resp.json().get("names", [])

    return metadata

# Fetch complete commit history (messages, author, date)
def fetch_commit_history(owner, repo, headers):
    commits = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        params = {"per_page": 100, "page": page}
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code != 200:
            break
        batch = resp.json()
        if not batch:
            break
        for c in batch:
            commit = c.get("commit", {})
            commits.append({
                "sha": c.get("sha"),
                "message": commit.get("message"),
                "author": (commit.get("author") or {}).get("name"),
                "date": (commit.get("author") or {}).get("date"),
            })
        page += 1
    return commits

# Fetch all items (issues or PRs) with full details
def fetch_items(owner, repo, headers, endpoint):
    items_list = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"
        params = {"state": "all", "per_page": 100, "page": page}
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code != 200:
            break
        batch = resp.json()
        if not batch:
            break
        for item in batch:
            # Common fields
            entry = {
                "id": item.get("id"),
                "number": item.get("number"),
                "title": item.get("title"),
                "user": item.get("user", {}).get("login"),
                "state": item.get("state"),
                "created_at": item.get("created_at"),
                "closed_at": item.get("closed_at"),
                "labels": [lbl.get("name") for lbl in item.get("labels", [])],
                "comments": item.get("comments"),
                "body": item.get("body")
            }
            # PR-specific fields
            if endpoint == "pulls":
                entry.update({
                    "merged_at": item.get("merged_at"),
                    "mergeable": item.get("mergeable")
                })
            items_list.append(entry)
        page += 1
    return items_list

# Append or initialize JSON file
def append_to_json(entry, filename="repos_metadata.json"):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            data = []
    else:
        data = []

    data.append(entry)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Appended repo: {entry['full_name']} (commits: {len(entry['commits'])}, issues: {len(entry['issues'])}, prs: {len(entry['prs'])})")

# Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scrape_github.py <github_repo_url>")
        sys.exit(1)
    url = sys.argv[1]
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        owner, repo = parse_github_url(url)
        meta = fetch_repo_metadata(owner, repo, headers)
        meta["commits"] = fetch_commit_history(owner, repo, headers)
        # Fetch full issues and PR lists
        meta["issues"] = fetch_items(owner, repo, headers, "issues")
        meta["prs"] = fetch_items(owner, repo, headers, "pulls")
        append_to_json(meta)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
