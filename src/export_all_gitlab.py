# Description: This script will clone all GitLab repositories from a GitLab instance.
# Author: Michael Launay
# Date: 2023-05-06
import os
import requests

# Set your GitLab URL and access token
GITLAB_HOST = "git.ecreall.com"
# For token creation, see https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html
ACCESS_TOKEN = "TOKEN FOR GITLAB-CE ROOT" # Fill with your own token
MAXIMUM_PROJECT_ID = 400 # Adapt this value to oversize your GitLab instance

# Set the directory where you want to clone the repositories
CLONE_DIR = "/home/michaellaunay/workspace"

# Create the clone directory if it doesn't exist
os.makedirs(CLONE_DIR, exist_ok=True)

# Create the base URL for the GitLab API
GITLAB_URL = f"https://{GITLAB_HOST}/api/v4/projects"

headers = {"PRIVATE-TOKEN": ACCESS_TOKEN}
# Try to access each project by ID
for i in range(1, MAXIMUM_PROJECT_ID):
    url = f"{GITLAB_URL}/{i}"
    # Retrieve the project details
    response = requests.get(f"{GITLAB_URL}/{i}", headers=headers, verify=False)
    # If the project doesn't exist, continue to the next ID
    if str(response.content, "utf-8").find("404 Project Not Found") > -1:
        continue
    print(f"{url =}")
    project = response.json()

    # Clone each project
    project_name = project["name"]
    project_path = project["path_with_namespace"]
    repository_url = project["ssh_url_to_repo"]

    # Clone the repository
    clone_path = os.path.join(CLONE_DIR, project_path)
    if not os.path.exists(os.path.join(project_path, ".git")):
        os.makedirs(clone_path, exist_ok=True)
        os.chdir(clone_path)
        os.system(f"git clone {repository_url}")

print("Cloning complete. All repositories have been cloned to", CLONE_DIR)

