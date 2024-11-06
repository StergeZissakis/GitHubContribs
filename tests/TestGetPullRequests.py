import responses
from fastapi.testclient import TestClient
from main import app
import testConfig as config

client = TestClient(app)

@responses.activate
def test_get_pull_requests():
    #Happy path
    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/users/{config.userName}/repos",
        json=[  {'name': f'{config.repositoryName}',    'default_branch': config.defaultBranchName } ],
        status=200
    )

    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/repos/{config.userName}/{config.repositoryName}/pulls?state=all&head={config.defaultBranchName}",
        json=[  {"created_at": "2024-10-17T00:00:00Z" } ],
        status=200
    )

    response = client.get(f"/pulls/{config.userName}?start_date=2024-10-16&end_date=2024-10-18")
    assert response.status_code == 200
    json = response.json()
    assert len(json["results"]) == 3
    assert json["results"][0] == 0
    assert json["results"][1] == 1
    assert json["results"][2] == 0

if __name__ == "__main__":
    test_get_pull_requests()