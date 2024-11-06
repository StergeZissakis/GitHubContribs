from TestGetCommits import test_get_commits
from TestGetIssues import test_get_issues
from TestGetIssues import test_get_issues_with_invalid_dates
from TestGetPullRequests import test_get_pull_requests
from TestGetRepositories import test_get_repos
from tests.TestGetRepositories import test_get_repos_pagination, test_get_repos_rate_limit

if __name__ == "__main__":
    test_get_repos()
    test_get_repos_pagination()
    test_get_repos_rate_limit()

    test_get_commits()

    test_get_issues()
    test_get_issues_with_invalid_dates()

    test_get_pull_requests()

