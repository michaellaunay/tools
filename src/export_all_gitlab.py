# Description: This script will clone all GitLab repositories from a GitLab instance.
# Author: Michael Launay
# Date: 2023-05-06
import os
import requests

# Set your GitLab URL and access token
GITLAB_HOST = "git.ecreall.com"
GITLAB_HOST = "gitlab.com/michaellaunay/test_gitlab"
# Fill with your own token
# For token creation, see https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html
ACCESS_TOKEN = "TOKEN FOR GITLAB-CE ROOT"
ACCESS_TOKEN = "glpat-otiAoU9NwHSy2zJxUJDp"
# Adapt this value to oversize your GitLab instance
MAXIMUM_PROJECT_ID = 400
MAXIMUM_PROJECT_ID = 4
# Set the directory where you want to clone the repositories
CLONE_DIR = "/home/michaellaunay/workspace"
CLONE_DIR = "/tmp/workspace"

def clone_project(gitlab_host:str=GITLAB_HOST,
    token:str=ACCESS_TOKEN,
    clone_dir:str=CLONE_DIR,
    maximum_project_id:int=MAXIMUM_PROJECT_ID) -> None:
    """Clone all GitLab repositories from a GitLab instance.
    Args:
        gitlab_host: The GitLab host name
        token: The GitLab access token
        clone_dir: The directory where you want to clone the repositories
        maximum_project_id: The maximum project ID to try to clone
    """

    headers = {"PRIVATE-TOKEN": token}
    # Create the base URL for the GitLab API
    gitlab_url = f"https://{gitlab_host}/api/v4/projects"

    # Try to access each project by ID
    for i in range(1, maximum_project_id):
        url = f"{gitlab_url}/{i}"
        # Retrieve the project details
        print(f"Try to clone {url =}")

        response = requests.get(f"{gitlab_url}/{i}", headers=headers, verify=False)
        # If the project doesn't exist, continue to the next ID
        if 200 > response.status_code or response.status_code >= 300 or str(response.content, "utf-8").find("404 Project Not Found") > -1:
            print(f"Project {i} not found, {response.status_code =} {response.reason =}")
            continue
        project = response.json()

        # Clone each project
        project_name = project["name"]
        project_path = project["path_with_namespace"]
        namespace_path = project["namespace"]["full_path"]
        repository_url = project["ssh_url_to_repo"]

        # Clone the repository
        clone_dir = os.path.join(CLONE_DIR, project_path)
        project_dir = os.path.join(CLONE_DIR, namespace_path)
        if not os.path.exists(os.path.join(clone_dir, ".git")):
            os.makedirs(project_dir, exist_ok=True)
            os.chdir(project_dir)
            os.system(f"git clone {repository_url}")
            print(f"Cloning {project_name} to {clone_dir}")
        else:
            os.chdir(clone_dir)
            os.system(f"git pull")
            print(f"Pulling {project_name} to {clone_dir}")

if __name__ == "__main__":
    import sys
    if sys.version_info < (3, 6):
        print("This script requires Python 3.6 or later")
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser(description="Clone all GitLab repositories from a GitLab instance.")
    parser.add_argument("--host", default=GITLAB_HOST, help="The GitLab host name")
    parser.add_argument("--token", default=ACCESS_TOKEN, help="The GitLab access token")
    parser.add_argument("--dir", default=CLONE_DIR, help="The directory where you want to clone the repositories")
    parser.add_argument("--maxid", default=MAXIMUM_PROJECT_ID, type=int, help="The maximum project ID to try to clone")
    args = parser.parse_args()


    # Create the clone directory if it doesn't exist
    os.makedirs(args.dir, exist_ok=True)
    # Clone all projects
    clone_project(args.host, args.token, args.dir, args.maxid)
    print("Cloning complete. All repositories have been cloned to", CLONE_DIR)

