from utils.rss import rss
import feedparser
import time
from datetime import datetime


def parser(ps):
    rss_link_all = []
    member_all = []
    cost = 0
    for r in rss:
        start_time = datetime.now()
        rp = feedparser.parse(r['link'])
        if not rp:
            continue
        try:
            rss_link_all_tmp = [{
                'id': r['id'],
                'title': et['title'],
                'link':et['link'],
                'home':rp['feed']['link'],
                'author':r['author'],
                'rss':r['link'],
                'date': time.strftime('%Y-%m-%d', et['published_parsed']),
                'tmstamp': time.mktime(et['published_parsed']),
            }
                for et in rp['entries']]

            member_all_tmp = [{'id': r['id'], 'author': r['author'], 'home': rp['feed']
                               ['link'], 'rss': r['link']}]

            rss_link_all = rss_link_all + rss_link_all_tmp
            member_all = member_all + member_all_tmp

            end_time = datetime.now()
            cost = cost + (end_time - start_time).microseconds / 1000.0
            print('parsing    {0:<40} cost    {1:<8}ms'.format(
                r['link'], (end_time - start_time).microseconds / 1000.0))
        except Exception as e:
            print('parsing    {0:<40} failed as {1}'.format(r['link'], e))
    print('{0:60}{1:<8}ms'.format('', cost))

    rss_link_all.sort(key=lambda item: item['tmstamp'], reverse=True)
    for member in member_all:
        for rss_link in rss_link_all:
            if rss_link['author'] == member['author']:
                member['date'] = rss_link['date']
                member['tmstamp'] = rss_link['tmstamp']
                break
    member_all.sort(key=lambda item: item['tmstamp'], reverse=True)

    ps['rssall'] = rss_link_all
    ps['member'] = member_all

    return ps


if __name__ == '__main__':
    parser({})
