from datetime import datetime
from pytz import timezone


def meta(ps):
    ps['meta'] = {
        'updatetime': datetime.now(tz=timezone('Asia/Shanghai')).isoformat(timespec='seconds'),
    }

    return ps
