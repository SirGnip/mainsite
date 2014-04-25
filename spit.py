import sys, os, os.path
from flask import request

def tag_pre(txt):
    return '<PRE>\n%s\n</PRE>' % txt

def _word_len_to_delay(word):
    'Given a word, return a delay'
    size = len(word)
    if size < 4:
        return 0
    elif size < 7:
        return 20
    elif size < 10:
        return 40
    else:
        return 100

class Chunk(object):
    # See if I can determine actual spritz timings for delays after periods, commas, newlines...
    PUNCTUATION_DELAY = 50
    PERIOD_DELAY = 100
    NEWLINE_DELAY = 200
    NEWLINE_TAG = 'THE_UNIQUE_NEWLINE_TAG'

    @staticmethod
    def factory(word):
        'Generate zero or more Chunks from the given word'
        result = []
        word = word.strip()
        delay = _word_len_to_delay(word)
        if word[-1] in ',;:-':
            result.append(Chunk(word, delay + Chunk.PUNCTUATION_DELAY))
        elif word[-1] == '.':
            result.append(Chunk(word, delay + Chunk.PERIOD_DELAY))
            result.append(Chunk('', 0))
        elif word == Chunk.NEWLINE_TAG:
            result.append(Chunk('', Chunk.NEWLINE_DELAY))
        else:
            result.append(Chunk(word, delay))
        return result
    
    def __init__(self, word, delay):
        self.word = word
        self.delay = delay
        self.timeline = 0
    def as_js(self):
        return '%d,%d,"%s"' % (self.timeline, self.delay, self.word)
        
def myspit(msg):
    d = os.path.dirname(__file__)
    os.chdir(d)
    html = open('spit_templ.html').read()

    # escape double quotes so they don't throw off the generated JavaScript
    msg = msg.replace('"', r'\"')
    # Encode newlines so I can convert it to a pause later in the process
    msg = msg.replace('\n', ' ' + Chunk.NEWLINE_TAG + ' ')
    # split on whitespace
    tokens = msg.split() # consecutive whitespace is treated as a single separator

    # convert tokens into chunks
    chunks = []
    for token in tokens:
        chunks += Chunk.factory(token)
    js_chunks = [c.as_js() for c in chunks]
    js_output = ','.join(js_chunks)

    output = '<ul>\n'
    for w in tokens:
        output += '<li>' + w + '</li>\n'
    output += '</ul>\n'
    output += '</ul>\n'
    return html % (output, js_output)


