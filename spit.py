import os, os.path

def tag_pre(txt):
    return '<PRE>\n%s\n</PRE>' % txt

def _word_len_to_delay(word):
    'Given a word, return a delay'
    size = len(word)
    if size < 6:
        return 0
    elif size < 7:
        return 20
    elif size < 12:
        return 40
    else:
        return 150 

class Chunk(object):
    # See if I can determine actual spritz timings for delays after periods, commas, newlines...
    PUNCTUATION_DELAY = 30
    PERIOD_DELAY = 220
    NEWLINE_DELAY = 300
    NEWLINE_TAG = 'THE_UNIQUE_NEWLINE_TAG'

    @staticmethod
    def factory(word, timecode):
        'Generate zero or more Chunks from the given word'
        result = []
        word = word.strip()
        delay = _word_len_to_delay(word)
        if word[-1] in ',;:-':
            result.append(Chunk(word, delay + Chunk.PUNCTUATION_DELAY, timecode))
        elif word[-1] == '.':
            result.append(Chunk(word, delay, timecode))
            result.append(Chunk('', Chunk.PERIOD_DELAY, timecode))
        elif word == Chunk.NEWLINE_TAG:
            result.append(Chunk('', Chunk.NEWLINE_DELAY, timecode))
        else:
            result.append(Chunk(word, delay, timecode))
        return result

    def __init__(self, word, delay, timecode):
        self.word = word
        self.delay = delay
        self.timecode = timecode

    def as_js(self):
        return '%d,%d,"%s"' % (self.timecode, self.delay, self.word)

def make_chunks(msg):
    # escape double quotes so they don't throw off the generated JavaScript
    msg = msg.replace('"', r'\"')
    # Encode newlines so I can convert it to a pause later in the process
    msg = msg.replace('\n', ' ' + Chunk.NEWLINE_TAG + ' ')
    # split on whitespace
    tokens = msg.split() # consecutive whitespace is treated as a single separator

    # convert tokens into chunks
    chunks = []
    for token in tokens:
        chunks += Chunk.factory(token, 0)
    return chunks

def serialize(msg):
    chunks = make_chunks(msg)
    js_chunks = [c.as_js() for c in chunks]
    return (chunks, ','.join(js_chunks))

def myspit(msg):
    d = os.path.dirname(__file__)
    os.chdir(d)
    html = open('spit_templ.html').read()

    chunks, js_output = serialize(msg)

    output = ''
#    output = '<ul>\n'
#    for c in chunks:
#        output += '<li>' + c.word + '</li>\n'
#    output += '</ul>\n'
#    output += '</ul>\n'
    return html % (output, js_output)

