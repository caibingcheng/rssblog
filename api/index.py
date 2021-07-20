from flask import Flask, render_template
from flaskext.markdown import Markdown
from datetime import datetime
from pytz import timezone
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

app = Flask(__name__, static_folder="../static",
            template_folder="../templates")
Markdown(app, extensions=['fenced_code'])

ps = {}
ps = markdown(ps, "about", "./templates/about.md")
ps = parser(ps)
ps = generator(ps)
ps = date(ps)

data = {
    'meta': {
        'updatetime': datetime.now(tz=timezone('Asia/Shanghai')).isoformat(timespec='seconds'),
    },
    'home': ps['home'],
    'member': ps['member'],
    'rss': ps['rss'],
    'about': ps['about'],
    'date': ps['date'],
}


@app.route('/')
def home():
    return render_template('home.html',
                           data=data['home'],
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
    return render_template('home.html',
                           data=data['date'][int(y)][int(m)],
                           meta=data['meta'],
                           val=int(time.time()))


@app.route('/rss')
def rss():
    return ps['rss'], 200, {'Content-Type': 'text/xml; charset=utf-8'}


if __name__ == '__main__':
    app.run()
