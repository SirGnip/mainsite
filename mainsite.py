import os, datetime
from flask import Flask, request

app = Flask(__name__)

BASE_URL = '/clipshout'

class ClipList(list):
    def __init__(self, max_len, *args):
        list.__init__(self, *args)
        self._max_len = max_len

    def push(self, obj):
        'push element onto the head, dropping any items off the end past max_len'
        if len(self) >= self._max_len:
            self.pop()
        self.insert(0, obj)

    def newest(self):
        if len(self) == 0:
            raise IndexError('Trying to get newest element in an empty ClipList')
        return self[0]


CLIP = ClipList(max_len=50)
CLIP.push('default clip')

def tag_pre(txt):
    return '<PRE>\n%s\n</PRE>' % txt

@app.route(BASE_URL + '/wsend')
def wsend():
    'web-send: a web-based way to send a clip'
    html = '''
    <title>wsend</title>
    <form action="send" method="post">
        <textarea name="clip" cols="40" rows="10"></textarea>
        <br>
        <input type="submit" value="Ok">
    </form>
    '''
    return html

@app.route(BASE_URL + '/wrecv')
def wrecv():
    'web-receive: a web-based way to receive the clip'
    html = '''
    <title>wrecv</title>\n'''
    stripped = CLIP.newest().strip()
    if stripped.startswith('http://') or stripped.startswith('https://') or stripped.startswith('www.'):
        html += '<a href="%s">%s</a>' % (stripped, stripped)
    else:
        html += tag_pre(CLIP.newest())
    return html

@app.route(BASE_URL + '/send', methods=['POST'])
def send():
    'API call to send a clip to server'
    print '=' * 40, 'push', request.method
    print type(request)
    old = CLIP.newest()
    new = request.form['clip']
    CLIP.push(new)
    return 'Changed clip from "%s" to "%s"' % (old, new)

@app.route(BASE_URL + '/recv')
def recv():
    'API call to get clip from server'
    return CLIP.newest()

@app.route(BASE_URL + '/status')
def status():
    items = []
    for item in CLIP:
        items.append(tag_pre(item))
    html = '<title>status</title>\n'
    html += '<HR>\n'.join(items)
    return html

@app.route(BASE_URL + '/debug')
def debug():
    html = '<title>debug</title>'
    return html + tag_pre(CLIP.newest()) + '<BR>======================<BR>' + repr(CLIP.newest())

####################### SPIT TEST
import spit
@app.route('/myspit')
def myspit():
    reload(spit)
    return spit.myspit(CLIP.newest())

