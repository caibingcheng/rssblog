from flask import Flask, render_template, redirect
import time
import os
import sys

root_path = os.path.abspath(__file__)
root_path = '/'.join(root_path.split('/')[:-2])
sys.path.append(root_path)

from utils.generator import generator
from utils.parser import parser

app = Flask(__name__, static_folder="../static",
            template_folder="../templates")
ps = parser()
ps = generator(ps)

data = {
    'meta': {
        'updatetime': time.ctime(),
    },
    'home': ps['home'],
    'member': ps['member'],
    'rss': ps['rss'],
}


@app.route('/')
def home():
    return render_template('home.html',
                           data=data)


@app.route('/member')
def member():
    return render_template('member.html',
                           data=data)


@app.route('/rss')
def rss():
    return ps['rss'], 200, {'Content-Type': 'text/xml; charset=utf-8'}


if __name__ == '__main__':
    app.run()
