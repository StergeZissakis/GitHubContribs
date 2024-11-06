# GitHubContribs

## Introduction
The task at hand was to create a REST API that consumes the GitHub's API to collect contributions' statistics on a per 
GitHub user basis within a range of dates.

### Requirements
The collected contributions comprise:

* Commits
* Issues
* PullRequests

The date range consists of a start date in the past and an end date which will be greater than start date; towards the 
future of start date.
<br>
If and end date is not provided, today's date is used.
<br>
If a start  date is not provided, it is the `end date - 365 days`
<br>
If a range is specified in the reverse order, an error is raised.

Processing of the GitHub responses must cover the following:

* Pagination of results; all results pages should be covered
* Rate Limiting: do not exceed the rate limit or cover for the case the rate limit is reached.

The requests towards the GitHub API must be parallelisable.
<br>
The final outcome of the requests should produce an array of size end date minus start date with a 1 day resolution, 
i.e. each element of the array contains the contributions for each day within the date range, starting from
 end date and ending in the start date. When the requests are parallelised the final result should be the sum of the
arrays returned by each request.

## Solution
The implementation involves a Python FastAPI interface with 3 main endpoints and an auxiliary one.
<br>
The auxiliary interface is the one that fetches the GitHub repositories for a user; called GetReposOfUser. This is 
needed as most of the rest of the requests use the internal code of GetReposOfUser to fetch the repositories and then 
loop through them, querying Commits, Issues and Pull Requests i.e. on a per repository basis.
<br>
Please note this functionality is exposed as an API endpoint for experimental and debugging purposes.
<br>
The results of this request is a JSON array of objects where each object contains the repository name and its default
branch name.

### GetCommitsOfRepo request
This requests returns an array of the Commits between start and end dates on a repository basis.
<br>
It uses the `/repos/{GitHubUserName}/{RepoNameOfUser}/commits?author={GitHubUserName}&sha={DefaultBranchOfRepo}` GitHub 
endpoint.
<br>
Once the commits have been collected, this endpoint filters them by creation date [endDate, startDate] to fill up the 
returned array.
<br>
The URI of this request is `/commits/{GitHubUserName}?start_date=&end_data=`

### GetPullRequestsOfRepo request
Similarly to the GetCommitsOfRepo request, this endpoint fetches pull requests on a per repository basis.
<br>
It uses the GitHub API endpoint: `/repos/{GitHubUserName}/{RepoNameOfUser}/pulls?state=all&head={DefaultBranchOfRepo}`.
<br>
The URI of this request is `/pulls/{GitHubUserName}?start_date=&end_data=`.
<br>
Again the results are filtered by creation date in the range [endDate, startDate]

### GetIssuesOfUser request
This works in the same way at the above two requests, however it utilises the search interface of the GitHub API and 
does not loop through all the user's repositories. This is due to the fact the GitHub `List repository issues` endpoint 
returns a mixture of Pull Requests and Issues as every Pull Request is also an Issue within this endpoint.
<br>
The GitHub URI used is: `/search/issues?q=author:{GitHubUserName}+type:issue`
<br>
The URI of this request is: `/issues/{GitHubUserName}?start_date=&end_data=`
<br>
Another particularity of this endpoint is that it may return results flagged as `incomplete results`. This means that 
the GitHub endpoint may not have been able to fetch all the information and a result this state will be depicted in the results
of this endpoint.

### Notes
The following apply to all the 3 main endpoint of this API, including the code that fetches a user's repositories.

#### Rate Limiting
The approach of choice is to wait for the specified period (by GitHub) when a request gets rate limited.
All the possible http response headers are considered in the following order:
* `Retry-After` in seconds
* `Retry-After` with RFC1123 date time
* `X-RateLimit-Reset` which is a UNIX epoch

Should none of above headers be present, the wait time is a configurable value in this API; it should never happen.
<br>
An extra wait time period (in seconds) is also added to each delay returned by the GitHub API. It is a configurable value
which defaults to 2 seconds; it is just in case countermeasure (better safe than sorry).

#### Pagination
Pagination is achieved via `Link` http response header. Among other information, this header contains the 'next' page 
field with the URL that will be used to fetch the next page.
<br>
The requests are being followed as far the 'next' field is present. When it is not, it means we have reached the last page.

## How to use
Clone this repo.
<br>
Create the docker image: `docker build -t fastapi-app . `
<br>
Run the docker instance: `docker run -d --name fastapi-app -p 8000:8000 fastapi-app`
<br>
Point your browser to the following url: [http://localhost:8000/app/index.html](http://localhost:8000/app/index.html)
<br>
Enjoy!

## Notes
Please refer to the README files in the subdirectories for a description of the contents.
Also please check the `refactoring` branch of this repository, for a more Objected Oriented and code reusability 
implementation variant of this branch's code. More on this on the README of that branch.




