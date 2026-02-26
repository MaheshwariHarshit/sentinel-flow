class JenkinsConnector:
    def get_build_info(self, job_name: str, build_id: str):
        print(f"Fetching Jenkins build {job_name} #{build_id}")
        return {
            "status": "FAILURE",
            "url": f"http://jenkins.local/job/{job_name}/{build_id}/console",
            "stage_failed": "Test_Integration",
            "commit_id": "a1b2c3d4"
        }

jenkins_connector = JenkinsConnector()
