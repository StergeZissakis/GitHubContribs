import Utils
from GitHubRequest import GitHubRequest

class GetCommitsOfRepo(GitHubRequest):
    url = ""
    userName = ""
    repoName = ""
    branchName = ""

    def __init__(self, user_name, repo_name, branch_name):
        self.userName = user_name
        self.repoName = repo_name
        self.branchName = branch_name
        self.url = f"https://api.github.com/repos/{self.userName}/{self.repoName}/commits?author={self.userName}&sha={self.branchName}"


    def processResults(self, response, result ):
        for commit in response.json():
            commitDate = commit["commit"]["author"]["date"].split("T")[0]  # extract only the date part
            commitDateTime = Utils.dateToDatetime(commitDate)
            result.append({"date": commitDateTime})
