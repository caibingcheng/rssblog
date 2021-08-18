import pandas


def fetch(url):
    return pandas.read_csv(url, encoding="utf-8")
