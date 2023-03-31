import requests
import sys
from datetime import datetime

def check_repo(repo):
    url = f"https://api.github.com/repos/{repo}"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        print(response.json()['message'])
        return False


def fetch_commit_date_by_url(url):
    headers = {'Accept': 'application/vnd.github.v3+json'}
  
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

def fetch_tags(repo):
    url = f"https://api.github.com/repos/{repo}/tags"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    response = requests.get(url, headers=headers)
    tags = response.json()
    tag_list = []
    for tag in tags:
        new_tag = {}
        print(tag['name'])
        new_tag['name'] = tag['name']
        new_tag['date'] = fetch_commit_date_by_url(tag['commit']['url'])
        new_tag['sha'] = tag['commit']['sha']
        new_tag['zipball_url'] = tag['zipball_url']
        new_tag['tarball_url'] = tag['tarball_url']
        tag_list.append(new_tag)
    sorted_tags = sorted(tag_list, key=lambda x: x['date'], reverse=True)
    return sorted_tags

if __name__ == "__main__":
    repository = str(sys.argv[1])
    print(repository)
    if not check_repo(repository):
        print("Repository not found")
        sys.exit(1)
    tags = fetch_tags(repository)
    print(tags)
