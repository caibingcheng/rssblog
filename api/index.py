from flask import Flask, render_template
import time, os, sys

root_path = os.path.abspath(__file__)
root_path = '/'.join(root_path.split('/')[:-2])
sys.path.append(root_path)

from utils.parser import parser

app = Flask(__name__, static_folder="../static", template_folder="../templates")
ps = parser()

data = {
    'meta': {
        'updatetime': time.ctime(),
    },
    'home': ps['home'],
    'member': ps['member'],
}

@app.route('/')
def home():
    return render_template('home.html',
                           data = data)

@app.route('/member')
def member():
    return render_template('member.html',
                           data = data)

if __name__ == '__main__':
    app.run()
