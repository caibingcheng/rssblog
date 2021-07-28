from flask import Flask, render_template, abort
from flaskext.markdown import Markdown
import time
import os
import sys

root_path = os.path.abspath(__file__)
root_path = '/'.join(root_path.split('/')[:-2])
sys.path.append(root_path)

from utils.generator import generator
from utils.parser import parser
from utils.markdown import markdown
from utils.date import date
from utils.meta import meta
from utils.friends import fds
from utils.randrss import randrss

app = Flask(__name__, static_folder="../static",
            template_folder="../templates")
Markdown(app, extensions=['fenced_code'])

ps = {}
ps = markdown(ps, "about", "./templates/about.md")
ps = parser(ps)
ps = generator(ps)
ps = date(ps)
ps = meta(ps)
ps = fds(ps)

data = ps

## default url

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html',
                           data=randrss(data['rssall'], 5),
                           meta=data['meta'],
                           val=int(time.time())), 404

@app.route('/')
def home():
    return render_template('home.html',
                           data=data['rssall'],
                           meta=data['meta'],
                           val=int(time.time()))

@app.route('/member')
def member():
    return render_template('member.html',
                           data=data['member'],
                           meta=data['meta'],
                           val=int(time.time()))

@app.route('/about')
def about():
    return render_template('about.html',
                           data=data['about'],
                           meta=data['meta'],
                           val=int(time.time()))


@app.route('/date')
def date():
    return render_template('date.html',
                           data=data['date'],
                           meta=data['meta'],
                           val=int(time.time()))


@app.route('/date/<y>/<m>')
def dateym(y, m):
    if int(y) not in data['date'].keys() or int(m) not in data['date'][int(y)].keys():
        abort(404)

    return render_template('home.html',
                           data=data['date'][int(y)][int(m)],
                           meta=data['meta'],
                           val=int(time.time()))

@app.route('/rss')
def rss():
    return data['rss'], 200, {'Content-Type': 'text/xml; charset=utf-8'}


### custom url

@app.route('/<id>')
def firends_home(id):
    if id not in data['friends']:
        abort(404)

    return render_template('home.html',
                           data=data['friends'][id],
                           meta=data['meta'],
                           id=id,
                           val=int(time.time()))

@app.route('/<id>/member')
def firends_member(id):
    if id not in data['friends-member']:
        abort(404)

    return render_template('member.html',
                           data=data['friends-member'][id],
                           meta=data['meta'],
                           id=id,
                           val=int(time.time()))

@app.route('/<id>/date')
def firends_date(id):
    if id not in data['friends-date']:
        abort(404)

    return render_template('date.html',
                           data=data['friends-date'][id],
                           meta=data['meta'],
                           id=id,
                           val=int(time.time()))


@app.route('/<id>/date/<y>/<m>')
def firends_dateym(id, y, m):
    if id not in data['friends-date']:
        abort(404)
    if int(y) not in data['friends-date'][id].keys() or int(m) not in data['friends-date'][id][int(y)].keys():
        abort(404)

    return render_template('home.html',
                           data=data['friends-date'][id][int(y)][int(m)],
                           meta=data['meta'],
                           id=id,
                           val=int(time.time()))

@app.route('/<id>/rss')
def friends_rss(id):
    if id not in data['friends-rss']:
        abort(404)
    return data['friends-rss'][id], 200, {'Content-Type': 'text/xml; charset=utf-8'}

if __name__ == '__main__':
    app.run()
