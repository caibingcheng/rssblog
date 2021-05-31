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
                    'date': time.strftime('%Y-%m-%d', et['published_parsed']),
                    'tmstamp': time.mktime(et['published_parsed']),} for et in rp['entries']]
        mb = mb + [{'author': r['author'], 'home': rp['feed']['link']}]
    rl.sort(key=lambda item: item['tmstamp'], reverse=True)
    random.shuffle(mb)

    return {'home': rl, 'member': mb}

if __name__ == '__main__':
    parser()
