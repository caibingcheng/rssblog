from datetime import datetime
from pytz import timezone

UPTIME = datetime.now(tz=timezone('Asia/Shanghai')).isoformat(timespec='seconds')

def meta():
    mt = {
        'updatetime': UPTIME,
    }

    return mt
