#!/usr/bin/env python3
""" Retrieve all LinkedIn comments and save them as Markdown files.
author: Michael Launay
mail: michaellaunay@ecreall.com
date: 2023-03-26
"""
import json
import requests
from datetime import datetime
import argparse
from packaging.version import parse
import os

def login_to_linkedin(email: str, password: str) -> requests.Session:
    """
    Logs in to LinkedIn with the specified credentials and returns a session object.
    params:
        email (str): The email address of the LinkedIn account.
        password (str): The password of the LinkedIn account.
    returns:
        requests.Session: The session object.
    """
    # LinkedIn API URL for retrieving comments
    api_url = "https://www.linkedin.com/voyager/api/comments?count=100&sort=CREATED&visibleToGuest=true"

    # HTTP headers required for authentication
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Csrf-Token": "ajax:1234567890"
    }

    # Login to LinkedIn with your credentials
    session = requests.Session()
    login_url = "https://www.linkedin.com/uas/login-submit"
    login_data = {
        "session_key": email,
        "session_password": password,
        "isJsEnabled": "false"
    }
    session.post(login_url, headers=headers, data=login_data)

    return session

def get_linkedin_comments(session: requests.Session) -> list:
    """
    Retrieves the LinkedIn comments written by the logged-in user and returns a list of dictionaries.
    params:
        session (requests.Session): The session object.
    returns:
        list: A list of dictionaries containing the comments.
    """
    # LinkedIn API URL for retrieving comments
    api_url = "https://www.linkedin.com/voyager/api/comments?count=100&sort=CREATED&visibleToGuest=true"

    # HTTP headers required for the LinkedIn API
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Csrf-Token": "ajax:1234567890"
    }

    # Retrieve the comments
    response = session.get(api_url, headers=headers)
    comments_data = json.loads(response.content)

    # Filter out the comments not written by the logged-in user
    comments = [comment for comment in comments_data["elements"] if comment["author"]["attributes"][0]["value"]["$deletedFields"] is None]

    return comments

def save_linkedin_comments(comments: list, path: str):
    """
    Saves the LinkedIn comments as Markdown files.
    params:
        comments (list): A list of dictionaries containing the comments.
    """
    # Create the Markdown files
    for comment in comments:
        # Extract the relevant information from the comment
        date = datetime.fromtimestamp(comment["created"]).strftime('%Y-%m-%d %H:%M:%S')
        content = comment["value"]["com.linkedin.voyager.feed.CommentV2"]["comment"].replace("\n", "\n\n")
        permalink = comment["permalink"]

        # Generate the Markdown content
        markdown_content = f"<!-- {permalink} -->\n\n**Date :** {date}\n\n{content}"

        # Save the comment to a Markdown file
        file_name = f"linkedin_comment_{comment['id']}.md"
        with open(os.path.join(path, file_name), "w", encoding="utf-8") as file:
            file.write(markdown_content)

        print(f"Comment {comment['id']} has been saved to file {file_name}.")

if __name__ == '__main__':
    # Parse command-line arguments
    TEST = True
    if TEST:
        from dataclasses import dataclass
        @dataclass
        class Args:
            email: str
            password: str
            path: str
        args = Args(
            email="michaellaunay@ecreall.com",
            password=input("Password: "),
            path="/tmp/comments")
    else:
        parser = argparse.ArgumentParser(description="Retrieve LinkedIn comments and save them in Markdown format.")
        parser.add_argument("-e", "--email", dest="email", type=str, help="Your LinkedIn email address.")
        parser.add_argument("-p", "--password", dest="password",type=str, help="Your LinkedIn password.")
        parser.add_argument("-d", "--dir", dest="path",type=str, help="The path where the comments will be saved.")
        parser.set_defaults(path=os.getcwd())
        args = parser.parse_args()

    # Login to LinkedIn
    session = login_to_linkedin(args.email, args.password)

    # Retrieve the comments written by the logged-in user
    comments = get_linkedin_comments(session)

    # Write comments in a Markdown file
    save_linkedin_comments(comments, args.path)
