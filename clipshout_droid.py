import android
droid = android.Android()
from gnp.utl import *
from gnp import net
import os
import sys
import datetime

'''PROBLEMS:
- logging isn't formatting properly as it isn't using the logging module
- opening a web url seems to block the script until the browser is minimized?
'''

class MyLogger(object):
    def __init__(self):
        fname = 'clipshout_scott.log'
        sys.__stdout__.write('Writing %s to %s\n' % (fname, os.getcwd()))
        self.file = open(fname, 'w', 0)

    def write(self, msg):
        sys.__stdout__.write(msg) # can't do print, otherwise it would infinitely loop because of redirection
        self.file.write(msg)
        
logger = MyLogger()

def startup():
    import sys
    sys.stdout = logger
    sys.stderr = sys.stdout
    
def get_local_ip():
    return net.get_local_ip()

def get_local_name():
    r=droid.getConstants('android.os.Build')
    CHK(r)
    return r.result['MODEL']
  
def get_clipboard():
    r=droid.getClipboard()
    CHK(r)
    return r.result
  
def set_clipboard(data):
    r=droid.makeToast('Clipshout set: %s' % data)
    CHK(r)
    r=droid.setClipboard(data)
    CHK(r)

def on_send_clipboard(data):
    droid.makeToast('Clipshout broadcasting: %s' % data)
    
def on_recv_clipboard(data):
    set_clipboard(data)
    
def on_recv_url(url):
    droid.makeToast('ClipShout opening URL: %s' % url.strip())
    #droid.webViewShow(url.strip()) # i don't 
    #droid.view(url.strip()) # seems to block the script until browser is minimized? Sometimes script is stalled even after minimizing browser.
    open_url(url)
    #droid.makeToast('ClipShout resuming after viewing URL')

def on_recv_path(path):
    print('Clipshout NO-OP: Open path:%s' % path.strip())
