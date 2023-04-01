import os
import requests
import sys
from datetime import datetime

def check_repo(repo, headers):
    url = f"https://api.github.com/repos/{repo}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return True
    else:
        print(response.json()['message'])
        return False


def fetch_commit_date_by_url(url, headers):
    response = requests.get(url, headers=headers)
  
    if response.ok:
        commit = response.json()
        if 'commit' in commit and 'author' in commit['commit']:
            date_str = commit['commit']['author']['date']
            date_obj = datetime.fromisoformat(date_str)
            commit_date = int(date_obj.timestamp())
            return commit_date
    print(f"Failed to fetch commit info: {response.status_code}")
    return 0

def fetch_tags(repo, headers, per_page=10, tag_limit=10):
    url = f"https://api.github.com/repos/{repo}/tags?per_page={per_page}"
    tag_list = []
    while url:
        response = requests.get(url, headers=headers)
        tags = response.json()
        if tag_limit != -1 and len(tag_list) >= tag_limit:
            break
        for tag in tags:
            new_tag = {}
            new_tag['name'] = tag['name']
            new_tag['date'] = fetch_commit_date_by_url(tag['commit']['url'], headers)
            new_tag['sha'] = tag['commit']['sha']
            new_tag['zipball_url'] = tag['zipball_url']
            new_tag['tarball_url'] = tag['tarball_url']
            tag_list.append(new_tag)
        if 'next' in response.links:
            url = response.links['next']['url']
        else:
            url = None
    sorted_tags = sorted(tag_list, key=lambda x: x['date'], reverse=True)
    return sorted_tags


if __name__ == "__main__":
    repository = str(sys.argv[1])
    per_page = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    tag_limit = int(sys.argv[3]) if len(sys.argv) > 3 else -1
    token = os.environ.get("GITHUB_TOKEN")
    headers = {'Accept': 'application/vnd.github.v3+json',
               'Authorization': f'token {token}'}
    if not check_repo(repository, headers):
        print("Repository not found")
        sys.exit(1)
    tags = fetch_tags(repository, headers, per_page, tag_limit)
    print(tags)
