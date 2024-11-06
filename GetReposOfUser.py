from time import sleep
import requests
import Utils
import config
from fastapi import HTTPException

class GetReposOfUser:
    url = ""
    userName = ""

    def __init__(self, user_name):
        self.userName = user_name
        self.url = f"https://api.github.com/users/{self.userName}/repos"

    def execute(self):
        requestRetries = config.rate_limit_retries
        result =[]

        while self.url is not None and requestRetries > 0:  # pagination and retries loop
            try:
                response = requests.get(self.url, headers=config.headers)
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                if err.response.status_code in (403, 429): # rate limit reached
                    sleep(Utils.getRateLimitRetryInSeconds(err.response.headers))
                    requestRetries -= 1
                    continue
                else:
                    raise HTTPException(status_code=err.response.status_code, detail=f"Get User Repos Failed:{err.response.text}")

            for repo in response.json():
                result.append({"name": repo["name"], "default_branch": repo["default_branch"]})

            self.url = Utils.parsePaginationHeader(response.headers)

        if  requestRetries ==0:
            status = "Rate Limit Retries Timeout"
        elif len(result) == 0:
            status = "No repositories found"
        else:
            status = "OK"
        return {'status': status, 'results': result}