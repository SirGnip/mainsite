import sys
sys.path.append('../python')
import urllib
import urllib2
import win32clip
import webbrowser

BASE_URL = r'http://juxtaflux.pythonanywhere.com/clipshout/'

'''
- get icons pinned to taskbar in vista, 7 and 8
    - how to pin shortcuts to taskbar: http://superuser.com/questions/100249/how-to-pin-either-a-shortcut-or-a-batch-file-to-the-new-windows-7-taskbar
- create simple icons
x for wget, convert clips that contain http into links (split on whitespace and do multiple links?)
x auto open URLs with "recv" 
- if a path/s, open explorers?
- get a native SL4A phone client working with urllib (non-2)
'''

def send():
    print '=' * 40, 'send'
    txt = win32clip.GetTextFromClipboard()
    print txt
    params = urllib.urlencode({
        'clip': txt,
    })
    resp = urllib.urlopen(BASE_URL + 'send', params).read()
    print 'RESPONSE:'
    print resp
    
def recv():
    print '=' * 40, 'recv'
    url_handle = urllib.urlopen(BASE_URL + 'recv')
    t = url_handle.read()
    url_handle.close()
    print t
    win32clip.SetTextOnClipboard(t)

    t = t.strip()
    if t.startswith('http://') or t.startswith('https://') or t.startswith('www.'):
        webbrowser.open(t)


if __name__ == '__main__':
    cmd = sys.argv[1].lower().strip()
    if cmd == 'send':
        send()
    elif cmd == 'recv':
        recv()
    else:
        raise Exception('Unknown command: "%s"' % cmd)
    