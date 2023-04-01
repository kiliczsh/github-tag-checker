import os
import requests
import sys
from datetime import datetime
import urllib.request
import zipfile

def download_file(url, file_name):
    response = urllib.request.urlopen(url)
    with open(file_name, 'wb') as f:
        f.write(response.read())

def unzip_file(zip_file, extract_path):
    with zipfile.ZipFile(zip_file) as zip_ref:
        zip_ref.extractall(extract_path)

def download_and_unzip(url, file_name, extract_path):
    print('Downloading file...')
    download_file(url, file_name)
    print('Unzipping file...')
    unzip_file(file_name, extract_path)

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
    extract_path = str(sys.argv[4]) if len(sys.argv) > 4 else str(os.getcwd())
    if not os.path.exists(extract_path):
        print('Creating directory: ' + extract_path)
        os.makedirs(extract_path)
    token = os.environ.get("GITHUB_TOKEN")
    headers = {'Accept': 'application/vnd.github.v3+json',
               'Authorization': f'token {token}'}
    if not check_repo(repository, headers):
        print("Repository not found")
        sys.exit(1)
    tags = fetch_tags(repository, headers, per_page, tag_limit)
    print(f"Fetched {len(tags)} tags")
    for tag in tags:
        print(f"Tag: {tag['name']}")
        print('Starting download and unzip of ' + tag['name'] + ' to ' + extract_path + '...')
        download_and_unzip(tag['zipball_url'], tag['name'] + '.zip', extract_path)
        print('Completed! ' + tag['name'] + ' to ' + extract_path + tag['name'] + '.zip...')
