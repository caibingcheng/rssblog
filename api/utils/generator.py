import datetime
import PyRSS2Gen

def generator(data):
    rss =PyRSS2Gen.RSS2(
        title="RSSBlog",
        link="https://rssblog.cn/",
        description="A Site for Blog RSS.",
        lastBuildDate = datetime.datetime.now(),

        items = [PyRSS2Gen.RSSItem(
            title=r['title'],
            link=r['link'],
            author=r['author'],
            # description=r['description'],
            pubDate=datetime.datetime.fromtimestamp(r['timestamp']),
        ) for r in data],
    )

    return "{}".format(rss.to_xml(encoding='utf-8'))