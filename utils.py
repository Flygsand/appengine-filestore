import email.utils as eut
from datetime import datetime
from time import mktime

def chunks(str, size):
    for i in xrange(0, len(str), size):
        yield str[i:i+size]

def http_format_date(time):
    if isinstance(time, datetime):
        time = mktime(time.utctimetuple())
    return eut.formatdate(time, usegmt=True)

def http_parse_date(str):
    if str:
        time = eut.mktime_tz(eut.parsedate_tz(str))
        return datetime.utcfromtimestamp(time)
