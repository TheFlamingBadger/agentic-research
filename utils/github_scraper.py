import os
import sys
import json
import requests
from datetime import datetime
from urllib.parse import urlparse

# -------------------------------------------------------------------------
# GitHub Repo Metadata & Activity Scraper with Duplication Checks
# -------------------------------------------------------------------------

# Constants for paths
data_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
summary_file = os.path.join(data_root, 'database_summary.json')

# Parse owner and repo from URL
def parse_github_url(repo_url):
    parsed = urlparse(repo_url)
    parts = parsed.path.strip("/").split("/")
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL: use https://github.com/owner/repo")
    return parts[0], parts[1]

# Ensure data directories exist
def ensure_repo_dir(repo_name):
    repo_dir = os.path.join(data_root, repo_name)
    os.makedirs(repo_dir, exist_ok=True)
    return repo_dir

# Append summary if not already present
def append_summary(entry):
    existing = []
    if os.path.exists(summary_file):
        try:
            with open(summary_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            existing = []
    # Check for duplicate by full_name
    if any(repo.get('full_name') == entry['full_name'] for repo in existing):
        print(f"Summary for {entry['full_name']} already exists; skipping append.")
        return
    existing.append(entry)
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)
    print(f"Appended summary for {entry['full_name']} to database_summary.json")

# Fetch repository summary metadata
def fetch_repo_metadata(owner, repo, headers):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return {
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
        "topics": data.get("topics", []),
        "default_branch": data.get("default_branch")
    }

# Generic fetcher for paginated endpoints
def fetch_paginated(owner, repo, headers, endpoint, item_mapper):
    items = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"
        resp = requests.get(url, headers=headers, params={"state": "all", "per_page": 100, "page": page})
        if resp.status_code != 200:
            break
        batch = resp.json()
        if not batch:
            break
        for item in batch:
            items.append(item_mapper(item))
        page += 1
    return items

# Mappers for commits, issues, prs, forks
commit_mapper = lambda c: {
    'sha': c.get('sha'),
    'message': c.get('commit', {}).get('message'),
    'author': (c.get('commit', {}).get('author') or {}).get('name'),
    'date': (c.get('commit', {}).get('author') or {}).get('date')
}
issue_mapper = lambda i: {
    'id': i.get('id'), 'number': i.get('number'), 'title': i.get('title'),
    'user': i.get('user', {}).get('login'), 'state': i.get('state'),
    'created_at': i.get('created_at'), 'closed_at': i.get('closed_at'),
    'labels': [lbl.get('name') for lbl in i.get('labels', [])],
    'comments': i.get('comments'), 'body': i.get('body')
}
pr_mapper = lambda p: dict(**issue_mapper(p), merged_at=p.get('merged_at'), mergeable=p.get('mergeable'))
fork_mapper = lambda f: {
    'id': f.get('id'), 'full_name': f.get('full_name'),
    'html_url': f.get('html_url'), 'created_at': f.get('created_at')
}

# Fetch README by raw markdown
def fetch_readme(owner, repo, branch):
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md"
    resp = requests.get(raw_url)
    return resp.text if resp.status_code == 200 else ''

# Write file if not exists
def write_file_if_missing(data, path, is_json=True):
    if os.path.exists(path):
        print(f"File {os.path.basename(path)} already exists; skipping.")
        return
    with open(path, 'w', encoding='utf-8') as f:
        if is_json:
            json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            f.write(data)
    print(f"Wrote {os.path.basename(path)}")

# Main
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python scrape_github.py <github_repo_url>")
        sys.exit(1)
    owner, repo = parse_github_url(sys.argv[1])
    token = os.getenv('GITHUB_TOKEN')
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f"token {token}"

    repo_dir = ensure_repo_dir(repo)

    # Summary
    summary = fetch_repo_metadata(owner, repo, headers)
    append_summary(summary)

    # Details
    write_file_if_missing(fetch_paginated(owner, repo, headers, 'commits', commit_mapper),
                          os.path.join(repo_dir, 'commits.json'))
    write_file_if_missing(fetch_paginated(owner, repo, headers, 'issues', issue_mapper),
                          os.path.join(repo_dir, 'issues.json'))
    write_file_if_missing(fetch_paginated(owner, repo, headers, 'pulls', pr_mapper),
                          os.path.join(repo_dir, 'prs.json'))
    write_file_if_missing(fetch_paginated(owner, repo, headers, 'forks', fork_mapper),
                          os.path.join(repo_dir, 'forks.json'))
    write_file_if_missing(fetch_readme(owner, repo, summary['default_branch']),
                          os.path.join(repo_dir, 'readme.md'), is_json=False)

    print(f"Data for {repo} processed in {repo_dir}")
