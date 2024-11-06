import Utils
from GitHubRequest import GitHubRequest

class GetPullRequestsOfRepo(GitHubRequest):
    url = ""
    userName = ""
    repoName = ""
    branchName = ""

    def __init__(self, user_name, repo_name, branch_name):
        self.userName = user_name
        self.repoName = repo_name
        self.branchName = branch_name
        self.url = f"https://api.github.com/repos/{self.userName}/{self.repoName}/pulls?state=all&head={self.branchName}"


    def processResults(self, response, result ):
        for pullRequest in response.json():
            pullRequestDate = pullRequest["created_at"].split("T")[0]  # extract only the date part
            pullRequestDateTime = Utils.dateToDatetime(pullRequestDate)
            result.append({"date": pullRequestDateTime})

