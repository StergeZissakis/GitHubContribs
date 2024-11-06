from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from GetCommitsOfRepo import GetCommitsOfRepo
from GetIssuesOfUser import GetIssuesOfUser
from GetPullRequestsOfRepo import GetPullRequestsOfRepo
from GetReposOfUser import GetReposOfUser
import uvicorn
import Utils

app = FastAPI()
app.mount("/app", StaticFiles(directory="www"), name="www")

#Experimental endpoint
@app.get("/repos/{userName}")
def get_repos(userName: str):

    req = GetReposOfUser(userName)
    return req.execute()

@app.get("/commits/{userName}")
def get_commits(userName: str, start_date: str = "", end_date: str = "" ):
    (numberofDays, startDateTime, endDateTime) = Utils.validateDateParameters(start_date, end_date)
    status = "OK"

    reposRequest = GetReposOfUser(userName)
    repos = reposRequest.execute()

    results = [0] * numberofDays # pre-allocate the array's memory and initialisation value 0
    if repos["status"] == "OK":
        for repo in repos["results"]:
            request = GetCommitsOfRepo(userName, repo["name"], repo["default_branch"])
            response = request.execute()
            if response["status"] != "OK":
                status = response["status"]
                break;
            for commit in response['results']:
                if startDateTime <= commit['date'] <= endDateTime:  # only if commit's date is within the sought daterange
                    resultsIndex = (endDateTime - commit['date']).days  # the diff of the date is the index
                    results[resultsIndex] += 1  # increment the commits in this position; range from [-365, today]
    else:
        status = repos["status"]

    return { 'status': status, 'results': results }

@app.get("/pulls/{userName}")
def get_pull_requests(userName: str, start_date: str = "", end_date: str = "" ):
    (numberofDays, startDateTime, endDateTime) = Utils.validateDateParameters(start_date, end_date)
    status = "OK"

    reposRequest = GetReposOfUser(userName)
    repos = reposRequest.execute()

    results = [0] * numberofDays # pre-allocate the array's memory and initialisation value 0
    if repos["status"] == "OK":
        for repo in repos['results']:
            request = GetPullRequestsOfRepo(userName, repo["name"], repo["default_branch"])
            response = request.execute()
            if response["status"] != "OK":
                status = response["status"]
                break;
            for pullRequest in response["results"]:
                if startDateTime <= pullRequest['date'] <= endDateTime:  # only if commit's date is within the sought daterange
                    resultsIndex = (endDateTime - pullRequest['date']).days  # the diff of the dates is the index
                    results[resultsIndex] += 1  # increment the pull requests in this position; range from [-365, today]
    else:
        status = repos["status"]

    return { 'status': status, 'results': results }

@app.get("/issues/{userName}")
def get_issues(userName: str, start_date: str = "", end_date: str = "" ):
    (numberofDays, startDateTime, endDateTime) = Utils.validateDateParameters(start_date, end_date)

    results = [0] * numberofDays # pre-allocate the array's memory and initialisation value 0

    request = GetIssuesOfUser(userName)
    response = request.execute()
    for issue in response["results"]:
        if startDateTime <= issue['date'] <= endDateTime:  # only if commit's date is within the sought daterange
            resultsIndex = (endDateTime - issue['date']).days  # the diff of the dates is the index
            results[resultsIndex] += 1  # increment the issues in this position; range from [-365, today]

    return { 'status': response["status"], 'results': results }