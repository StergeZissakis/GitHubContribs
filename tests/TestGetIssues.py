import responses
from fastapi.testclient import TestClient
from main import app
import testConfig as config

client = TestClient(app)

@responses.activate
def test_get_issues():
    #Happy path
    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/search/issues?q=author:{config.userName}+type:issue",
        json={ "incomplete_results": "false",
               "items" : [ {"created_at": "2024-10-18T00:00:00Z"},
                           {"created_at": "2024-10-17T00:00:00Z"},
                           {"created_at": "2024-10-16T00:00:00Z"},
                           {"created_at": "2024-10-15T00:00:00Z"},
                           {"created_at": "2024-10-14T00:00:00Z"},
                         ]
            },
        status=200
    )

    response = client.get(f"/issues/{config.userName}?start_date=2024-10-14&end_date=2024-10-18")
    assert response.status_code == 200
    json = response.json()
    assert len(json["results"]) == 5
    for i in range(0, 5):
        assert json["results"][i] == 1

    #Happy path with different start date
    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/search/issues?q=author:{config.userName}+type:issue",
        json={ "incomplete_results": "false",
               "items" : [ {"created_at": "2024-10-18T00:00:00Z"},
                           {"created_at": "2024-10-17T00:00:00Z"},
                           {"created_at": "2024-10-16T00:00:00Z"},
                           {"created_at": "2024-10-15T00:00:00Z"},
                           {"created_at": "2024-10-14T00:00:00Z"},
                         ]
            },
        status=200
    )

    response = client.get(f"/issues/{config.userName}?start_date=2024-10-15&end_date=2024-10-18")
    assert response.status_code == 200
    json = response.json()
    assert len(json["results"]) == 4
    for i in range(0, 4):
        assert json["results"][i] == 1

    #Happy path with different end date
    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/search/issues?q=author:{config.userName}+type:issue",
        json={ "incomplete_results": "false",
               "items" : [ {"created_at": "2024-10-18T00:00:00Z"},
                           {"created_at": "2024-10-17T00:00:00Z"},
                           {"created_at": "2024-10-16T00:00:00Z"},
                           {"created_at": "2024-10-15T00:00:00Z"},
                           {"created_at": "2024-10-14T00:00:00Z"},
                         ]
            },
        status=200
    )

    response = client.get(f"/issues/{config.userName}?start_date=2024-10-14&end_date=2024-10-17")
    assert response.status_code == 200
    json = response.json()
    assert len(json["results"]) == 4
    for i in range(0, 4):
        assert json["results"][i] == 1

    #Happy path with different start and end dates
    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/search/issues?q=author:{config.userName}+type:issue",
        json={ "incomplete_results": "false",
               "items" : [ {"created_at": "2024-10-18T00:00:00Z"},
                           {"created_at": "2024-10-17T00:00:00Z"},
                           {"created_at": "2024-10-16T00:00:00Z"},
                           {"created_at": "2024-10-15T00:00:00Z"},
                           {"created_at": "2024-10-14T00:00:00Z"},
                         ]
            },
        status=200
    )

    response = client.get(f"/issues/{config.userName}?start_date=2024-10-15&end_date=2024-10-17")
    assert response.status_code == 200
    json = response.json()
    assert len(json["results"]) == 3
    for i in range(0, 3):
        assert json["results"][i] == 1


    #Happy path with single date
    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/search/issues?q=author:{config.userName}+type:issue",
        json={ "incomplete_results": "false",
               "items" : [ {"created_at": "2024-10-18T00:00:00Z"},
                           {"created_at": "2024-10-17T00:00:00Z"},
                           {"created_at": "2024-10-16T00:00:00Z"},
                           {"created_at": "2024-10-15T00:00:00Z"},
                           {"created_at": "2024-10-14T00:00:00Z"},
                         ]
            },
        status=200
    )

    response = client.get(f"/issues/{config.userName}?start_date=2024-10-16&end_date=2024-10-16")
    assert response.status_code == 200
    json = response.json()
    assert len(json["results"]) == 1
    assert json["results"][0] == 1

    #Happy path with gap in dates
    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/search/issues?q=author:{config.userName}+type:issue",
        json={ "incomplete_results": "false",
               "items" : [  {"created_at": "2024-10-19T00:00:00Z"},
                            {"created_at": "2024-10-18T00:00:00Z"},
                            {"created_at": "2024-10-14T00:00:00Z"},
                            {"created_at": "2024-10-13T00:00:00Z"},
                            ]
            },
        status=200
    )

    response = client.get(f"/issues/{config.userName}?start_date=2024-10-14&end_date=2024-10-18")
    assert response.status_code == 200
    json = response.json()
    assert len(json["results"]) == 5
    assert json["results"][0] == 1
    for i in range(1, 4):
        assert json["results"][i] == 0
    assert json["results"][4] == 1

@responses.activate
def test_get_issues_with_invalid_dates():
    #Unhappy path with reverse dates
    responses.add(
        method=responses.GET,
        url = f"https://api.github.com/search/issues?q=author:{config.userName}+type:issue",
        json={ "incomplete_results": "false",
               "items" : [  {"created_at": "2024-10-19T00:00:00Z"},
                            {"created_at": "2024-10-18T00:00:00Z"},
                            {"created_at": "2024-10-14T00:00:00Z"},
                            {"created_at": "2024-10-13T00:00:00Z"},
                            ]
            },
        status=200
    )

    response = client.get(f"/issues/{config.userName}?start_date=2024-10-18&end_date=2024-10-14")
    assert response.status_code == 400


if __name__ == "__main__":
    test_get_issues()
    test_get_issues_with_invalid_dates()