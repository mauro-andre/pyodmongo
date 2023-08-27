import requests


def get_latest_release_version(repo_owner, repo_name):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest'
    response = requests.get(url)
    data = response.json()
    return data.get('tag_name')


if __name__ == "__main__":
    repo_owner = "mauro-andre"
    repo_name = "pyodmongo"
    version = get_latest_release_version(repo_owner, repo_name)
    print(version)
