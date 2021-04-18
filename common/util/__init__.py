import collections

import pytz

__all__ = (
    "DocInfo",
    "KST",
)

KST = pytz.timezone("Asia/Seoul")
DocInfo = collections.namedtuple("DocInfo", "id, json")
