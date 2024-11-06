api_key = ""

headers = {
    'Authorization': f'token {api_key}',
    'Accept': 'application/vnd.github.v3+json',  # using V3 API
}

rate_limit_retries = 3
extraWaitSeconds = 2
defaultRetryIntervalInSeconds = 60
