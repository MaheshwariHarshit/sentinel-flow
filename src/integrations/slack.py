import os
from src.core.config import config

class SlackConnector:
    def __init__(self):
        self.enabled = config.integrations.slack.enabled
        self.channel = config.integrations.slack.channel
        self.token = os.getenv("SLACK_BOT_TOKEN", "dummy_token")
        
    def send_situation_report(self, incident_id: str, summary: str, rca_preview: str):
        if not self.enabled:
            return
            
        message = f"""
*Sentinel-Flow Incident Report: {incident_id}*
*Summary:* {summary}
*RCA Preview:* {rca_preview}
"""
        print(f"Sending Slack Message to {self.channel}: \n{message}")

slack_connector = SlackConnector()
