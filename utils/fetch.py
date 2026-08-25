import pandas
import requests
import re
from io import StringIO

def fetch_raw(url):
    is_url = re.compile(r"^https?://")
    if not is_url.match(url):
        with open(url, "r", encoding="utf-8") as f:
            return f.read()
    raw = requests.get(url)
    print(f"get source {raw.status_code} from {url}")
    if raw.status_code != 200:
        raise Exception("get source error")
    return raw.text

FETCH_METHOD = {
    "csv": lambda url: pandas.read_csv(StringIO(fetch_raw(url)), encoding="utf-8"),
    "xml": fetch_raw,
}

def fetch(url, type="csv"):
    return FETCH_METHOD[type](url)