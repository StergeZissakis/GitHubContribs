import calendar
import datetime
from fastapi import HTTPException
import config


def validateDateParameters(start_date, end_date):
    if len(end_date) == 0:
        endDateTime = datetime.date.today()
    else:
        endDateTime = dateToDatetime(end_date)

    if len(start_date) == 0:
        startDateTime = endDateTime - datetime.timedelta(days=365)
    else:
        startDateTime = dateToDatetime(start_date)

    if startDateTime > endDateTime:
        raise HTTPException(status_code=400, detail=f"Start date cannot be greater than end date")

    return ((endDateTime - startDateTime).days + 1, startDateTime, endDateTime)

def dateToDatetime(date):
    parts = date.split('-')
    if len(parts) != 3:
        raise HTTPException(status_code=400, detail=f"Wrong date format:'{date}'")
    return datetime.date(int(parts[0]), int(parts[1]), int(parts[2]))

# Looks for Link header in response headers.
# if found and contains a rel="next" field, then the equivalent URL is returned
# if not found, None is returned.
def parsePaginationHeader(responseHeaders):
    if responseHeaders.get('Link', None) is None:
        return None

    linkHeaders = responseHeaders.get('Link').split(',')
    for linkHeader in linkHeaders:
        parts = linkHeader.split(';')
        rel = parts[1].strip().split('=')[1][1:-1]
        if rel == 'next':
            return parts[0].strip()[1:-1] # the URL

    return None

def getRateLimitRetryInSeconds(responseHeaders):
    if 'Retry-After' in responseHeaders.keys():
        secondsOrDate = responseHeaders.get('Retry-After')
        try:
            return int(secondsOrDate) + config.extraWaitSeconds
        except ValueError: # not seconds but date time
            parts = secondsOrDate.split(' ')
            day = int(parts[1])
            month = int(list(calendar.month_abbr).index(parts[2])) # convert from abbreviation to numeric
            year = int(parts[3])
            (hours, minutes, seconds) = parts[4].split(':')
            delayDatetime = datetime.datetime(year=year, month=month, day=day, hour=int(hours), minute=int(minutes), second=int(seconds), tzinfo=datetime.timezone.utc)
            now = datetime.datetime.now(tz=datetime.timezone.utc)
            return (delayDatetime - now).seconds + config.extraWaitSeconds
    else: # fall back to the X-RateLimit-Reset header
        delayEpoch = responseHeaders.get('X-RateLimit-Reset', None)
        if delayEpoch is None: # no choice but to retry again in a pre-configured amount of time
            return config.defaultRetryIntervalInSeconds
        else:
            delayDatetime = datetime.datetime.fromtimestamp(int(delayEpoch), tz=datetime.timezone.utc)
            now = datetime.datetime.now(tz=datetime.timezone.utc)
            return (delayDatetime - now).seconds + config.extraWaitSeconds


