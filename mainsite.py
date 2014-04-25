import os, datetime
from flask import Flask, request
import clipswap

app = Flask(__name__)

clip = 'default clip'

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
    stripped = clip.strip()
    if stripped.startswith('http://') or stripped.startswith('https://') or stripped.startswith('www.'):
        html += '<a href="%s">%s</a>' % (stripped, stripped)
    else:
        html += tag_pre(clip)
    return html

@app.route('/clipswap/send', methods=['POST'])
def send():
    'API call to send a clip to server'
    global clip
#    reload(clipswap)
    print '=' * 40, 'push', request.method
    print type(request)
    print dir(request)
    old = clip
    clip = request.form['clip']
    return 'Changed clip from "%s" to "%s"' % (old, clip)

@app.route('/clipswap/recv')
def recv():
    'API call to get clip from server'
    return clip

@app.route('/clipswap/status')
def status():
    return 'Clip: %s' % clip

@app.route('/clipswap/debug')
def debug():
    html = '<title>debug</title>'
    return html + tag_pre(clip) + '<BR>======================<BR>' + repr(clip)
