import datetime

userName = "sterge"
defaultBranchName = "master"
repositoryName = "repo"

def getRFCdatetimeInFuture(secondsAhead):
    future = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=secondsAhead)
    ret = future.strftime('%a, %d %b %Y %H:%M:%S GMT')
    return ret

def getEpochInFuture(secondsAhead):
    future = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=secondsAhead)
    return int(future.timestamp())