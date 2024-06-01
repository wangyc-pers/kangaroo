import datetime


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc)


def datetime_to_str(dt, format=None):
    if format is None:
        return dt.isoformat()
    else:
        return dt.strftime(format)
