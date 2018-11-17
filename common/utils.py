
def now():
    '''get current utc time'''
    from datetime import datetime
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S%z')


def epoch():
    import time
    return int(time.time())


def getShortUid():
    '''get uuid 4, shortened to first six values'''
    import uuid
    u = str(uuid.uuid4())
    return u[:6]


# print(shortUuid())
