from datetime import datetime

def date(ps, inkey=None, outkey=None, locale=True):
    rl = ps['rssall' if not inkey else inkey]
    date = {}
    for r in rl:
        dt = datetime.strptime(r['date'], '%Y-%m-%d')
        date[dt.year] = {
            1:[],
            2:[],
            3:[],
            4:[],
            5:[],
            6:[],
            7:[],
            8:[],
            9:[],
            10:[],
            11:[],
            12:[],
        }
    for r in rl:
        dt = datetime.strptime(r['date'], '%Y-%m-%d')
        date[dt.year][dt.month].append(r)

    if locale:
        ps['date' if not outkey else outkey] = date
        return ps
    else:
        return date