from flask import Flask, render_template, abort, request, url_for, redirect
from flaskext.markdown import Markdown
import time
import random
import json
import os
import sys
root_path = os.path.abspath(__file__)
root_path = '/'.join(root_path.split('/')[:-2])
sys.path.append(root_path)

from utils.init import RssblogSource, SOURCE_BASE
from utils.generator import generator
from utils.parser import parser, hash_url
from utils.fetch import fetch
from utils.meta import meta
from utils.markdown import markdown

print("init rssblog source")
rs = RssblogSource()
print("init rssblog source done")

print("init flask")
app = Flask(__name__, static_folder="../static",
            template_folder="../templates")
print("init flask done")

print("init markdown")
Markdown(app, extensions=['fenced_code'])
md = markdown("./README.md", locale=True)
print("init markdown done")

print("init meta")
meta = meta()
print("init meta done")


def gen_pagination(page, pages):
    PAGE = 3
    start, end = page - PAGE, page + PAGE
    start = 1 if start < 1 else start
    end = pages if end > pages else end
    pagination = {
        "page": page,
        "pages": int(pages),
        "has_prev": page > 1,
        "has_next": page < pages,
        "start": start,
        "end": end,
    }
    return pagination


@app.template_filter("is_today")
def is_today(date):
    return meta["today"] == date


@app.template_filter("is_in24h")
def is_in24h(timestamp):
    return abs(meta["timestamp"] - timestamp) < 24 * 60 * 60


# default url


@app.errorhandler(404)
def not_found(id):
    page = random.randint(1, rs.url["all"])
    url = (SOURCE_BASE + 'all/{}.csv').format(page)
    data = parser(fetch(url))
    return render_template('404.html',
                           id=id,
                           data=data,
                           meta=meta,
                           val=int(time.time())), 404


@app.route('/')
def home_default():
    return home(1)


@app.route('/<int:page>/')
def home(page=1, id=None, pages=rs.url["all"], base_url='all', endpoint='home'):
    if page > int(pages):
        abort(404)
    url = (SOURCE_BASE + base_url + '/{}.csv').format(page)
    data = parser(fetch(url))

    args = request.args
    method = args.get("method")
    method = "html" if not method else method
    if method == "raw":
        raw_data = json.dumps(data, ensure_ascii=False)
        return "{}({})".format(args.get("jsoncallback"), raw_data) if "jsoncallback" in args.keys() else raw_data.encode('utf8')

    return render_template('home.html',
                           data=data,
                           meta=meta,
                           id=id,
                           pagination=gen_pagination(page, pages),
                           endpoint=endpoint,
                           val=int(time.time()))


@app.route('/member/')
def member_default():
    return member(1)


@app.route('/member/<int:page>/')
def member(page=1, id=None, pages=rs.url["member"], base_url='member', endpoint='member'):
    if page > int(pages):
        abort(404)
    url = (SOURCE_BASE + base_url + '/{}.csv').format(page)
    data = hash_url(parser(fetch(url)))
    return render_template('member.html',
                           data=data,
                           meta=meta,
                           id=id,
                           pagination=gen_pagination(page, pages),
                           endpoint=endpoint,
                           val=int(time.time()))


@app.route('/member/<string:hash_url>/')
def member_home_default(hash_url, page=1):
    return member_home(hash_url, page=1)


@app.route('/member/<string:hash_url>/<int:page>/')
def member_home(hash_url, page=1, id=None, base_url='source', endpoint='member_home'):
    if hash_url not in rs.url["source"].keys():
        abort(404)
    if page > rs.url["source"][hash_url]:
        abort(404)

    data = []
    args = request.args
    sample = args.get("sample")
    sample = False if not sample else True
    method = args.get("method")
    method = "html" if not method else method
    count = args.get("count")
    try:
        count = -1 if not count else int(count)
    except:
        abort(404)

    if not sample:
        url = (SOURCE_BASE + base_url + '/{0}/{1}.csv').format(hash_url, page)
        data = parser(fetch(url))
    else:
        page = random.randint(1, rs.url["source"][hash_url])
        url = (SOURCE_BASE + base_url + '/{0}/{1}.csv').format(hash_url, page)
        data = parser(fetch(url))

    if count > 0:
        data = random.sample(data, min(count, len(data)))

    if method == "raw":
        raw_data = json.dumps(data, ensure_ascii=False)
        return "{}({})".format(args.get("jsoncallback"), raw_data) if "jsoncallback" in args.keys() else raw_data.encode('utf8')

    return render_template('home.html',
                           data=data,
                           meta=meta,
                           id=id,
                           pagination=gen_pagination(
                               page, rs.url["source"][hash_url]),
                           endpoint=endpoint,
                           kwargs={'hash_url': hash_url},
                           val=int(time.time()))


@app.route('/date/')
def date(data=rs.url['date'], id=None):
    return render_template('date.html',
                           data=data,
                           meta=meta,
                           id=id,
                           val=int(time.time()))


@app.route('/date/<int:y>/<int:m>/')
def date_year_month_default(y, m):
    return date_year_month(y, m, 1)


@app.route('/date/<int:y>/<int:m>/<int:page>/')
def date_year_month(y, m, page=1, id=None, date=rs.url["date"], base_url='date', endpoint='date_year_month', kwargs=None):
    year_ok = None
    for year in date:
        if year['year'] == y:
            year_ok = year
            break
    if not year_ok:
        print("not year ok", y, date)
        abort(404)
    is_month_ok = m in year_ok['month'].keys()
    if not is_month_ok:
        print("not month ok", m)
        abort(404)
    is_page_ok = page <= year_ok['month'][m]
    if not is_page_ok:
        print("not page ok", page)
        abort(404)

    url = (SOURCE_BASE + base_url +
           '/{0:04d}{1:02d}/{2}.csv').format(y, m, page)
    data = parser(fetch(url))
    return render_template('home.html',
                           data=data,
                           meta=meta,
                           id=id,
                           pagination=gen_pagination(
                               page, year_ok['month'][m]),
                           endpoint=endpoint,
                           kwargs=kwargs if kwargs else {'y': y, 'm': m},
                           val=int(time.time()))


@app.route('/about/')
def about():
    abort(404)
    return render_template('about.html',
                           data=md,
                           meta=meta,
                           val=int(time.time()))


@app.route('/rss/')
def rss(base_url='all'):
    url = SOURCE_BASE + base_url + '/rss.xml'
    return fetch(url, type="xml"), 200, {'Content-Type': 'text/xml; charset=utf-8'}


@app.route('/immediate/')
def immediate():
    rs.immediate()
    return 200


# ### custom url


@app.route('/<id>/')
def user_home_default(id):
    return user_home(id, 1)


@app.route('/<id>/<int:page>/')
def user_home(id, page=1):
    user_ok = False
    for user in rs.url["user"]:
        if id == user["user"]:
            user_ok = user
            break
    if not user_ok:
        abort(404, id)
    return home(page=page,
                id=id,
                pages=user_ok["all"],
                base_url='user/' + user_ok['user']+'/all',
                endpoint='user_home')


@app.route('/<id>/member/')
def user_member_default(id):
    return user_member(id, 1)


@app.route('/<id>/member/<int:page>/')
def user_member(id, page=1):
    user_ok = False
    for user in rs.url["user"]:
        if id == user["user"]:
            user_ok = user
            break
    if not user_ok:
        abort(404, id)
    return member(page=page,
                  id=id,
                  pages=user_ok["member"],
                  base_url='user/' + user_ok['user']+'/member',
                  endpoint='user_member')


@app.route('/<id>/member/<string:hash_url>/')
def user_member_home_default(id, hash_url):
    return user_member_home(id, hash_url, 1)


@app.route('/<id>/member/<string:hash_url>/<int:page>/')
def user_member_home(id, hash_url, page=1):
    user_ok = False
    for user in rs.url["user"]:
        if id == user["user"]:
            user_ok = user
            break
    if not user_ok:
        abort(404, id)
    return member_home(page=page,
                       id=id,
                       hash_url=hash_url,
                       endpoint='user_member_home')


@app.route('/<id>/date/')
def user_date(id):
    user_ok = False
    for user in rs.url["user"]:
        if id == user["user"]:
            user_ok = user
            break
    if not user_ok:
        abort(404, id)
    return date(data=user_ok['date'], id=id)


@app.route('/<id>/date/<int:y>/<int:m>/')
def user_date_year_month_default(id, y, m):
    return user_date_year_month(id, y, m, 1)


@app.route('/<id>/date/<int:y>/<int:m>/<int:page>/')
def user_date_year_month(id, y, m, page=1):
    user_ok = False
    for user in rs.url["user"]:
        if id == user["user"]:
            user_ok = user
            break
    if not user_ok:
        abort(404, id)
    return date_year_month(y=y,
                           m=m,
                           page=page,
                           id=id,
                           date=user_ok["date"],
                           base_url='user/' + user_ok['user']+'/date',
                           endpoint='user_date_year_month',
                           kwargs={'y': y, 'm': m})


@app.route('/<id>/rss/')
def user_rss(id):
    user_ok = False
    for user in rs.url["user"]:
        if id == user["user"]:
            user_ok = user
            break
    if not user_ok:
        abort(404, id)
    return rss(base_url='user/' + user_ok['user']+'/all')


if __name__ == '__main__':
    app.run()
