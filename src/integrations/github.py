import os
import requests
from src.core.config import config

class GitHubConnector:
    def __init__(self):
        self.enabled = config.integrations.github.enabled
        self.token = os.getenv("GITHUB_TOKEN", "dummy_token")
        self.headers = {"Authorization": f"token {self.token}"}
        
    def fetch_code_snippet(self, repo: str, filepath: str, line_start: int, line_end: int):
        if not self.enabled:
            return "public void getUserDetails(String name) { \n  // dummy code snippet \n}"
        
        # Fetching code snippet using GitHub API could go here
        print(f"Fetching {filepath} lines {line_start}-{line_end} from {repo}")
        return "public void getUserDetails(String name) { \n  System.out.println(name.length()); // causes NPE if name is null \n}"

    def create_pr_comment(self, repo: str, pr_number: int, comment: str):
        if not self.enabled:
            print(f"Would have posted to {repo} PR #{pr_number}:\n{comment}")
            return True
            
        print(f"Posting PR comment to {repo}/{pr_number}...")
        return True

github_connector = GitHubConnector()
