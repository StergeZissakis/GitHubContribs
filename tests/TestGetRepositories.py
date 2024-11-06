import time

import responses
from fastapi.testclient import TestClient

import testConfig as config
from main import app

client = TestClient(app)

@responses.activate
def test_get_repos():
    # happy path
    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/users/{config.userName}/repos",
        json=[  {'name': f'{config.repositoryName}',    'default_branch': config.defaultBranchName },
                {'name': 'repo2',                       'default_branch': config.defaultBranchName },
                {'name': 'repo3',                       'default_branch': config.defaultBranchName }
        ],
        status=200
    )

    response = client.get(f"/repos/{config.userName}")
    assert response.status_code == 200
    json = response.json()
    assert len(json["results"]) == 3
    assert json["results"][0]["name"] == config.repositoryName

@responses.activate
def test_get_repos_pagination():
    # Initial request with Link header
    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/users/{config.userName}/repos",
        json=[  {'name': f'{config.repositoryName}',    'default_branch': config.defaultBranchName },
                {'name': 'repo2',                       'default_branch': config.defaultBranchName },
                {'name': 'repo3',                       'default_branch': config.defaultBranchName }
        ],
        headers={'Link' : f'<https://api.github.com/users/{config.userName}/repos?per_page=3&page=2>;rel="next"'},
        status=200
    )

    # Subsequent request with the next/last page
    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/users/{config.userName}/repos?per_page=3&page=2",
        json=[  {'name': 'repo4', 'default_branch': config.defaultBranchName },
                {'name': 'repo5', 'default_branch': config.defaultBranchName },
                {'name': 'repo6', 'default_branch': config.defaultBranchName }
        ],
        status=200
    )


    response = client.get(f"/repos/{config.userName}")
    assert response.status_code == 200
    json = response.json()
    assert len(json["results"]) == 6
    assert json["results"][0]["name"] == config.repositoryName
    assert json["results"][5]["name"] == 'repo6'

@responses.activate
def test_get_repos_rate_limit():
    # With Retry-After header being in seconds
    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/users/{config.userName}/repos",
        headers={'Retry-After' : '5'},
        status=403
    )

    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/users/{config.userName}/repos",
        json=[  {'name': f'{config.repositoryName}',    'default_branch': config.defaultBranchName } ],
        status=200
    )

    startTime = time.time()
    response = client.get(f"/repos/{config.userName}")
    endTime = time.time()
    assert response.status_code == 200
    assert endTime - startTime >= 5 # ensure the test took the required time
    json = response.json()
    assert len(json["results"]) == 1
    assert json["results"][0]["name"] == config.repositoryName

    # With Retry-After header being an RFC1123 datetime
    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/users/{config.userName}/repos",
        headers={'Retry-After' : config.getRFCdatetimeInFuture(5)},
        status=403
    )

    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/users/{config.userName}/repos",
        json=[  {'name': f'{config.repositoryName}',    'default_branch': config.defaultBranchName } ],
        status=200
    )

    startTime = time.time()
    response = client.get(f"/repos/{config.userName}")
    endTime = time.time()
    assert response.status_code == 200
    assert endTime - startTime >= 5 # ensure the test took the required time
    json = response.json()
    assert len(json["results"]) == 1
    assert json["results"][0]["name"] == config.repositoryName

    # With X-RateLimit-Reset header being an epoch
    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/users/{config.userName}/repos",
        headers={'X-RateLimit-Reset' : str(config.getEpochInFuture(5))},
        status=403
    )

    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/users/{config.userName}/repos",
        json=[  {'name': f'{config.repositoryName}',    'default_branch': config.defaultBranchName } ],
        status=200
    )

    startTime = time.time()
    response = client.get(f"/repos/{config.userName}")
    endTime = time.time()
    assert response.status_code == 200
    assert endTime - startTime >= 5 # ensure the test took the required time
    json = response.json()
    assert len(json["results"]) == 1
    assert json["results"][0]["name"] == config.repositoryName

    # Test the retries timeout
    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/users/{config.userName}/repos",
        headers={'Retry-After' : '1'},
        status=403
    )

    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/users/{config.userName}/repos",
        headers={'Retry-After' : '1'},
        status=403
    )

    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/users/{config.userName}/repos",
        headers={'Retry-After' : '1'},
        status=403
    )

    response = client.get(f"/repos/{config.userName}")
    assert response.status_code == 200
    json = response.json()
    assert json["status"] == "Rate Limit Retries Timeout"



if __name__ == "__main__":
    test_get_repos()
    test_get_repos_pagination()
    test_get_repos_rate_limit()