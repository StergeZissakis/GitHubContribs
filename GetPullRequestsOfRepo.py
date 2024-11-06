from time import sleep
import requests
import Utils
import config
from fastapi import HTTPException

class GetPullRequestsOfRepo:
    url = ""
    userName = ""
    repoName = ""
    branchName = ""

    def __init__(self, user_name, repo_name, branch_name):
        self.userName = user_name
        self.repoName = repo_name
        self.branchName = branch_name
        self.url = f"https://api.github.com/repos/{self.userName}/{self.repoName}/pulls?state=all&head={self.branchName}"

    def execute(self):
        requestRetries = config.rate_limit_retries
        result =[]

        while self.url is not None and requestRetries > 0: # pagination and retries loop
            try:
                response = requests.get(self.url, headers=config.headers)
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                if err.response.status_code == 409: # repo is empty
                    return {'status': "OK", 'results': []}
                if err.response.status_code in (403, 429): # rate limit reached
                    sleep(Utils.getRateLimitRetryInSeconds(err.response.headers))
                    requestRetries -= 1
                    continue
                else:
                    raise HTTPException(status_code=err.response.status_code, detail=f"Get Pull Requests of Repo:[{err.response.text}]")

            for pullRequest in response.json():
                pullRequestDate = pullRequest["created_at"].split("T")[0]  # extract only the date part
                pullRequestDateTime = Utils.dateToDatetime(pullRequestDate)
                result.append({"date": pullRequestDateTime})

            self.url = Utils.parsePaginationHeader(response.headers)

        if requestRetries == 0:
            status = "Rate Limit Retries Timeout"
        elif len(result) == 0:
            status = "No Pull Requests found"
        else:
            status = "OK"
        return {'status': status, 'results': result}