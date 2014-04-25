import sys, os, os.path
from flask import request

NEWLINE_TAG = 'MY_UNIQUE_NEWLINE_TAG'

def tag_pre(txt):
    return '<PRE>\n%s\n</PRE>' % txt

def myspit(msg):
    d = os.path.dirname(__file__)
    os.chdir(d)
    html = open('spit_templ.html').read()

    msg = msg.replace('"', r'\"')
    # Add delay for carriage returns
    msg = msg.replace('\n', ' ' + NEWLINE_TAG + ' ')
    wrds = msg.split()
    tokens = []
    for w in wrds:
        if w.strip()[-1] in ',;:-':
            tokens.append('%d,%d,"%s"' % (0, 100, w))
        elif w.strip()[-1] == '.':
            tokens.append('%d,%d,"%s"' % (0, 100, w))
            tokens.append('%d,%d,"%s"' % (0, 100, ''))
        elif w.strip() == NEWLINE_TAG:
            tokens.append('%d,%d,"%s"' % (0, 200, ''))
        else:
            tokens.append('%d,%d,"%s"' % (0, 0, w))

    output = '<ul>\n'
    for w in wrds:
        output += '<li>' + w + '</li>\n'
    output += '</ul>\n'
    output += '</ul>\n'
    return html % (output, ','.join(tokens))
