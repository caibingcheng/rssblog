from utils.rss import rss
import feedparser, time, random

def parser(ps):
    rl = []
    mb = []
    for r in rss:
        print('parsing', r['link'])
        rp = feedparser.parse(r['link'])
        if not rp: continue
        rl = rl + [{'title': et['title'],
                    'link':et['link'],
                    'home':rp['feed']['link'],
                    'author':r['author'],
                    'rss':r['link'],
                    # 'description': et['description'] if 'description' in et else '',
                    'date': time.strftime('%Y-%m-%d', et['published_parsed']),
                    'tmstamp': time.mktime(et['published_parsed']),} for et in rp['entries']]
        mb = mb + [{'author': r['author'], 'home': rp['feed']['link'], 'rss': r['link']}]
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
