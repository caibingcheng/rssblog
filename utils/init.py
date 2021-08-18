import json
import requests
SOURCE_BASE = "https://raw.githubusercontent.com/caibingcheng/rssblog-source/public/"
SOURCE_URL = SOURCE_BASE + "stats.min.json"
SOURCE_JSON = json.loads(requests.get(SOURCE_URL).text)
BTACH = SOURCE_JSON["batch"]
URL = SOURCE_JSON["urls"]

def init_date(DATE):
    YEAR = []
    for date in DATE:
        month = {}
        for m in date[1]:
            month[int(m[0])] = int(m[1])
        YEAR.append({
            "year": int(date[0]),
            "month": month,
        })
    YEAR.sort(key = lambda x: x.get('year', 0), reverse = True)
    return YEAR

URL["date"] = init_date(URL["date"])
for user in URL["user"]:
    user["date"] = init_date(user["date"])