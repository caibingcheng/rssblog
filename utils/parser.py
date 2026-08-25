import json
import hashlib


def hash(url):
    md5 = hashlib.md5()
    md5.update(url.encode('utf-8'))
    return md5.hexdigest()


def parser(df):
    return json.loads(df.to_json(orient="records"))


def hash_url(urls):
    for url in urls:
        rss_hash = url.get("rss_hash")
        url["hash"] = rss_hash if rss_hash else hash(url["rss"].strip(" ").strip("/"))
    return urls
