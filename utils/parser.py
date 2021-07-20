from utils.rss import rss
import feedparser, time, random
from datetime import datetime

def parser(ps):
    rl = []
    mb = []
    cost = 0
    for r in rss:
        start_time = datetime.now()
        rp = feedparser.parse(r['link'])
        if not rp: continue
        try:
            trl = [{'title': et['title'],
                        'link':et['link'],
                        'home':rp['feed']['link'],
                        'author':r['author'],
                        'rss':r['link'],
                        # 'description': et['description'] if 'description' in et else '',
                        'date': time.strftime('%Y-%m-%d', et['published_parsed']),
                        'tmstamp': time.mktime(et['published_parsed']),} for et in rp['entries']]
            tmb = [{'author': r['author'], 'home': rp['feed']['link'], 'rss': r['link']}]
            rl = rl + trl
            mb = mb + tmb
            end_time = datetime.now()
            cost = cost + (end_time - start_time).microseconds / 1000.0
            print('parsing    {0:<40} cost    {1:<8}ms'.format(r['link'], (end_time - start_time).microseconds / 1000.0))
        except Exception as e:
            print('parsing    {0:<40} failed as {1}'.format(r['link'], e))
    print('{0:60}{1:<8}ms'.format('', cost))
    rl.sort(key=lambda item: item['tmstamp'], reverse=True)

    for member in mb:
        for r in rl:
            if r['author'] == member['author']:
                member['date'] = r['date']
                member['tmstamp'] = r['tmstamp']
                break
    # random.shuffle(mb)
    mb.sort(key=lambda item: item['tmstamp'], reverse=True)
    ps['home'] = rl
    ps['member'] = mb

    return ps

if __name__ == '__main__':
    parser({})
