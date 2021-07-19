from utils.rss import rss
import feedparser, time, random

def parser():
    rl = []
    mb = []
    for r in rss:
        rp = feedparser.parse(r['link'])
        rl = rl + [{'title': et['title'],
                    'link':et['link'],
                    'home':rp['feed']['link'],
                    'author':r['author'],
                    # 'description': et['description'] if 'description' in et else '',
                    'date': time.strftime('%Y-%m-%d', et['published_parsed']),
                    'tmstamp': time.mktime(et['published_parsed']),} for et in rp['entries']]
        mb = mb + [{'author': r['author'], 'home': rp['feed']['link']}]
    rl.sort(key=lambda item: item['tmstamp'], reverse=True)

    for member in mb:
        for r in rl:
            if r['author'] == member['author']:
                member['date'] = r['date']
                member['tmstamp'] = r['tmstamp']
                break
    # random.shuffle(mb)
    mb.sort(key=lambda item: item['tmstamp'], reverse=True)

    return {'home': rl, 'member': mb}

if __name__ == '__main__':
    parser()
