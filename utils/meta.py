from datetime import datetime
from pytz import timezone


def meta():
    mt = {
        'updatetime': datetime.now(tz=timezone('Asia/Shanghai')).isoformat(timespec='seconds'),
    }

    return mt