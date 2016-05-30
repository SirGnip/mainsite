import os, datetime
from flask import Flask, request, Response, render_template

BASE_URL = '/clipshout'
app = Flask(__name__, static_folder='static', static_url_path=BASE_URL + '/static')


def _add_cors_headers(response):
    """Add CORS headers to given response object
    Reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS
    Flask-specific reference: http://www.davidadamojr.com/handling-cors-requests-in-flask-restful-apis/"""
    # I don't know if this is absolutely necessary, but I'm adding it to see if it gets rid of occasional failures
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')

def resp_with_cors(txt):
    resp = Response(txt)
    _add_cors_headers(resp)
    return resp


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
    body = '''
    <form action="send" method="post">
        <input type="submit" value="Ok" style="height:3.0em;width:100%">
        <br>
        <textarea name="clip" cols="40" rows="25"></textarea>
    </form>'''
    return resp_with_cors(render_template('clipshout_generic.html', PAGE_TITLE='wsend', BODY_TEXT=body))

@app.route(BASE_URL + '/wrecv')
def wrecv():
    'web-receive: a web-based way to receive the clip'
    stripped = CLIP.newest().strip()
    if stripped.startswith('http://') or stripped.startswith('https://') or stripped.startswith('www.'):
        text = '<a href="%s">%s</a>' % (stripped, stripped)
    else:
        text = '<pre>' + CLIP.newest() + '</pre>'
    return resp_with_cors(render_template('clipshout_wrecv.html', WRECV_BODY=text))

@app.route(BASE_URL + '/send', methods=['POST'])
def send():
    'API call to send a clip to server'
    print '=' * 40, 'push', request.method
    print type(request)
    old = CLIP.newest()
    new = request.form['clip']
    CLIP.push(new)
    body = 'Changed clip from "%s" to "%s"' % (old, new)
    return resp_with_cors(render_template('clipshout_generic.html', PAGE_TITLE='send', BODY_TEXT=body))

@app.route(BASE_URL + '/recv')
def recv():
    'API call to get clip from server'
    return resp_with_cors(CLIP.newest())

@app.route(BASE_URL + '/status')
def status():
    items = []
    for item in CLIP:
        items.append(tag_pre(item))
    html = '<title>status</title>\n'
    html += '<HR>\n'.join(items)
    return resp_with_cors(render_template('clipshout_generic.html', PAGE_TITLE='status', BODY_TEXT=html))

@app.route(BASE_URL + '/debug')
def debug():
    html = '<title>debug</title>'
    html = html + tag_pre(CLIP.newest()) + '<BR>======================<BR>' + repr(CLIP.newest())
    return resp_with_cors(render_template('clipshout_generic.html', PAGE_TITLE='debug', BODY_TEXT=html))

import spritz
@app.route(BASE_URL + '/spritz')
def myspritz():
    reload(spritz)
    return spritz.spritz_clip(app, CLIP.newest())


####################### SPIT TEST
import spit
@app.route('/myspit')
def myspit():
    reload(spit)
    return spit.myspit(CLIP.newest())


'''PythonAnywhere does not require app.run() as it runs this file based on config in the "Web" tab on the PythonAnywhere dashboard.
But, it is still safe t orun app.run() in a function like this as it won't get run when PythonAnywhere imports the file.
Reference: https://help.pythonanywhere.com/pages/Flask/'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)