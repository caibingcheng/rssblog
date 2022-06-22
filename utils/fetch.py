import pandas
import requests

FETCH_METHOD = {
    "csv": lambda url: pandas.read_csv(url, encoding="utf-8"),
    "xml": lambda url: requests.get(url).text
}

def fetch(url, type="csv"):
    return FETCH_METHOD[type](url)