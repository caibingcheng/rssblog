import json
import os
import time
import requests
import buffercache
SOURCE_BASE = "https://raw.githubusercontent.com/caibingcheng/rssblog-source/public/"
SOURCE_URL = SOURCE_BASE + "stats.min.json"


class RssblogSouce(object):
    def __init__(self):
        self._bc = buffercache.BufferCache(timeout=1000*60*60*3).set_getter(self._update)

    def _update(self):
        self._source_json = json.loads(requests.get(SOURCE_URL).text)
        print("[{}] update rssblog source".format(os.getpid()), time.time())
        self._batch = self._source_json["batch"]
        self._url = self._source_json["urls"]

        self._url["source"] = self._source(self._url["source"])
        self._url["date"] = self._date(self._url["date"])
        for user in self._url["user"]:
            user["date"] = self._date(user["date"])
        return self._url, self._batch

    @staticmethod
    def _date(date_ls):
        year = []
        for date in date_ls:
            month = {}
            for m in date[1]:
                month[int(m[0])] = int(m[1])
            year.append({
                "year": int(date[0]),
                "month": month,
            })
        year.sort(key=lambda x: x.get('year', 0), reverse=True)
        return year

    @staticmethod
    def _source(sources):
        source_mp = {}
        for source in sources:
            source_mp[source[0]] = source[1]
        return source_mp

    @property
    def url(self):
        url, _ = self._bc.update().get()
        return url

    @property
    def batch(self):
        _, batch = self._bc.update().get()
        return batch
