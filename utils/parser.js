var rss_parser = {
    run: function (src, method, options = {type: 'rss'}) {
        if (options.type == 'rss')
        {
            let data = this[method].article(src);
            return this._finish(data)
        }

        if (options.type == 'member')
        {
            let data = this[method].member(src);
            return data
        }
    },

    sort: function (data) {
        data.sort(function (d1, d2) {
            return d2.timestamp - d1.timestamp
        })
        let i = 1;
        data.map(each => {
            each.index = i;
            i = i + 1;
        })
        return data
    },

    _finish: function (data) {
        data.map(each => {
            let date = new Date(each.pubDate)
            each.timestamp = date.getTime()
            let month = date.getMonth() + 1
            month = month < 10 ? ('0' + month) : ('' + month)
            let ddate = date.getDate()
            ddate = ddate < 10 ? ('0' + ddate) : ('' + ddate)
            each.date = date.getFullYear() + '-' + month + '-' + ddate
        })

        return data
    },

    'rss': {
        article: function (src) {
            let data = []
            let item = src.rss.channel.item
            item.map(each => {
                data.push({
                    pubDate: each.pubDate,
                    link: each.link,
                    home: src.rss.channel.link,
                    title: each.title,
                    date: '',
                    timestamp: 0,
                    author: '',
                    index: 0
                })
            })
            return data
        },
        member: function (src) {
            let data = src.rss.channel
            let date = new Date(data.lastBuildDate)
            return {
                title: data.title,
                link: data.link,
                date: date.toISOString()
            }
        }
    },

    'atom': {
        article: function (src) {
            let data = []
            let item = src.feed.entry
            item.map(each => {
                data.push({
                    pubDate: each.published,
                    link: each.link.href,
                    home: src.feed.id,
                    title: each.title,
                    date: '',
                    timestamp: 0,
                    author: '',
                    index: 0
                })
            })
            return data
        },
        member: function (src) {
            let data = src.feed
            let date = new Date(data.updated)
            return {
                title: data.title,
                link: data.id,
                date: date.toISOString()
            }
        }
    }
}

export default rss_parser