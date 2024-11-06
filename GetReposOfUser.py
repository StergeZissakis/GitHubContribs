from GitHubRequest import GitHubRequest

class GetReposOfUser(GitHubRequest):
    url = ""
    userName = ""

    def __init__(self, user_name):
        self.userName = user_name
        self.url = f"https://api.github.com/users/{self.userName}/repos"

    def processResults(self, response, result ):
        for repo in response.json():
            result.append({"name": repo["name"], "default_branch": repo["default_branch"]})
