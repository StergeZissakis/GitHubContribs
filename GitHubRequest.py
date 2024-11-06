from abc import abstractmethod
from time import sleep
import requests
from fastapi import HTTPException
import Utils
import config


class GitHubRequest:
    url = str

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
                    raise HTTPException(status_code=err.response.status_code, detail=f"Get Commits of Repo:[{err.response.text}]")

            self.processResults(response, result)

            self.url = Utils.parsePaginationHeader(response.headers)

        if requestRetries == 0:
            status = "Rate Limit Retries Timeout"
        elif len(result) == 0:
            status = "No entries found"
        else:
            status = "OK"
        return {'status': status, 'results': result}

    @abstractmethod
    def processResults(self, response, result ):
        pass
