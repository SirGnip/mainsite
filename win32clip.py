'''
Code taken from win32Wrap.py
'''

import time
import win32clipboard
import win32clipboard
import pywintypes

##### Standalone functions
MAX_RETRIES = 300
RETRY_DELAY = 0.01

def _open_clipboard_and_retry():
	'''It is possible to attempt to open the clipboard and have it fail. This
	function encapsulates a retry mechanism.
	REPRO: Have code in a tight loop that opens/reads/closes the clipboard.  While
	that is running, manually copy some text into the clipboard and then hold
	down Ctrl+V to repeatedly paste the text into Notepad.  Hold Ctrl+V down for a
	few seconds and you will be able to reliably cause an Exception.  But, with
	this retry mechanism, you need to be pasting a very large clipboard with very
	tight loops to have a chance of getting an Exception.'''    
	for ct in range(MAX_RETRIES):
		try:
			win32clipboard.OpenClipboard()
		except pywintypes.error:
			time.sleep(RETRY_DELAY)
		else:
			return
	raise Exception('Access denied when attempting to OpenClipboard(). Retried %d times.' % MAX_RETRIES)

def GetTextFromClipboard():
	_open_clipboard_and_retry()
	try:
		text = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
	except TypeError:
		text = ''
	win32clipboard.CloseClipboard()
	return(text)

def SetTextOnClipboard(text):
	'''write to clipboard'''
	_open_clipboard_and_retry()
	win32clipboard.EmptyClipboard()
	win32clipboard.SetClipboardText(text)
	win32clipboard.CloseClipboard()