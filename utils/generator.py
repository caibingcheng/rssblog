import datetime
import PyRSS2Gen

def generator(ps):
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
            pubDate=datetime.datetime.fromtimestamp(r['tmstamp']),
        ) for r in ps['home']],
    )
    ps['rss'] = "{}".format(rss.to_xml(encoding='utf-8'))

    return ps

if __name__ == '__main__':
    import time, os, sys

    root_path = os.path.abspath(__file__)
    root_path = '/'.join(root_path.split('/')[:-2])
    sys.path.append(root_path)

    from parser import parser
    ps = {}
    ps = parser(ps)
    ps = generator(ps)
    # print(ps['rss'])

    import sys
    ps_size = sys.getsizeof(ps)
    print(ps_size)