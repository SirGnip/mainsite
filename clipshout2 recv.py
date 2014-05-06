import android
droid = android.Android()
import urllib
import clipshout_droid

BASE_URL = r'http://juxtaflux.pythonanywhere.com/clipshout/'

if __name__ == '__main__':
    print type(droid)
    f = urllib.urlopen(BASE_URL + 'recv')
    clip = f.read()
    print clip
    clipshout_droid.set_clipboard(clip)

    cleaned = clip.strip().lower()
    if cleaned.startswith('http://') or cleaned.startswith('https://') or cleaned.startswith('www.'):
        clipshout_droid.on_recv_url(clip.strip())

    print 'done.......'
    