from time import sleep
import requests
import Utils
import config
from fastapi import HTTPException

class GetIssuesOfUser:
    url = ""
    userName = ""

    def __init__(self, user_name):
        self.userName = user_name
        self.url = f"https://api.github.com/search/issues?q=author:{self.userName}+type:issue"

    def execute(self):
        requestRetries = config.rate_limit_retries
        result =[]
        incompleteResults = False

        while self.url is not None and requestRetries > 0: # pagination and retries loop
            try:
                response = requests.get(self.url, headers=config.headers)
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                if err.response.status_code in (403, 429): # rate limit reached
                    sleep(Utils.getRateLimitRetryInSeconds(err.response.headers))
                    requestRetries -= 1
                    continue
                else:
                    raise HTTPException(status_code=err.response.status_code, detail=f"Get Issues of User:[{err.response.text}]")

            if response.json()['incomplete_results'] is True:
                incompleteResults = True

            for issue in response.json()['items']:
                issueDate = issue["created_at"].split("T")[0]  # extract only the date part
                issueDateTime = Utils.dateToDatetime(issueDate)
                result.append({"date": issueDateTime})

            self.url = Utils.parsePaginationHeader(response.headers) # check for paginated results

        status = "OK"
        if requestRetries == 0:
            status = "Rate Limit Reached"
        elif incompleteResults:
            status = "Incomplete results"
        return { 'status': status, 'results': result }