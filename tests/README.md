# Functional Tests
The functional tests were implemented as different and independant Python scripts. I did not incorporate them into any 
Testing suite, for simplicity reasons.
<br>
They use assertions to verify the results. It all goes well you should see no output. If something fails, the script 
stops and prints the point of the failure.
<br>
The Python `responses` package was used to mock GitHub requests/responses.
<br>
There are tests for the code involved, including the 'GetReposOfUser' code.

## testConfig.py
Contains static data used across the tests, such as GitHub username, repo name and branch.
<br>
Also included are some utility functions that facilitate date conversion between different formats.

## TestGetCommits.py
It contains only one happy path test for the endport `/commits/{GitHubUserName}`.

## TestGetIssues.py
This test involves a happy path oif the `/issues/{GitHubUserName}` endpoint along with testing on the startr and end 
date paramters. It covers all the cases for the date range.
<br>
Once the date range handling code is common across all requests, these tests are not repeated in the rest of the tests.

## TestGetPullRequests.py
This tests happy path of the `/pulls/{GitHubUserName}` only.

## TestGetRepositories.py
This tests the internal code of fetch a user's repositories.
<br>
It also covers all possible scenarios for rate limiting and pagination.
<br>
It utilises the auxiliary endpoint '/repos/{GitHubUserName}'.

# Usage
You may run each test from within your Python virtual environment, by issuing: `python TestGetCommits.py`, etc.