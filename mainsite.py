import os, datetime
from flask import Flask, request
import clipswap

app = Flask(__name__)

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


CLIP = ClipList(max_len=20)
CLIP.push('default clip')

def tag_pre(txt):
    return '<PRE>\n%s\n</PRE>' % txt

@app.route('/clipswap/wsend')
def wsend():
    'web-send: a web-based way to send a clip'
    html = '''
    <title>wsend</title>
    <form action="http://juxtaflux.pythonanywhere.com/clipswap/send" method="post">
        <textarea name="clip" cols="40" rows="10"></textarea>
        <br>
        <input type="submit" value="Ok">
    </form>
    '''
    return html

@app.route('/clipswap/wrecv')
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

@app.route('/clipswap/send', methods=['POST'])
def send():
    'API call to send a clip to server'
#    reload(clipswap)
    print '=' * 40, 'push', request.method
    print type(request)
    print dir(request)
    old = CLIP.newest()
    new = request.form['clip']
    CLIP.push(new)
    return 'Changed clip from "%s" to "%s"' % (old, new)

@app.route('/clipswap/recv')
def recv():
    'API call to get clip from server'
    return CLIP.newest()

@app.route('/clipswap/status')
def status():
    items = []
    for item in CLIP:
        items.append(tag_pre(item))
    html = '<title>status</title>\n'
    html += '<HR>\n'.join(items)
    return html

@app.route('/clipswap/debug')
def debug():
    html = '<title>debug</title>'
    return html + tag_pre(CLIP.newest()) + '<BR>======================<BR>' + repr(CLIP.newest())

