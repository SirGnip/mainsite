import urllib
import clipshout_droid
import android
droid = android.Android()

# Reference: http://stackoverflow.com/questions/14062338/retrieving-data-via-post-request
txt = clipshout_droid.get_clipboard()
txt = txt.encode('ascii', 'ignore')
data = {'clip': txt}
url = r'http://juxtaflux.pythonanywhere.com/clipshout/send'
s = urllib.urlopen(url, bytes(urllib.urlencode(data)))
print s.read()
droid.makeToast('Clipshout sent: ' + txt)