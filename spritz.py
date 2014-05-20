import os.path
import private_config
import json
from flask import render_template

# Handling the Spritzing of a URL:
# - PythonAnywhere server cant read it because of whitelist
# - can't do an ajax query client side because of cross-site limitations
# - but it seems like giving spritz the URL works just fine (if i'm ok with 
#   the caching of content that the Spritz servers seem to do).
def is_web_url(url):
    url = url.strip().lower()
    return url.startswith('http://') or url.startswith('https://') or url.startswith('www.')

def spritz_clip(flask_app, clip):
    'Spritz the current clip'
    config = private_config.as_dict()

    if is_web_url(clip):
        config['SPRITZ_DATA_URL_ATTR'] = 'data-role="spritzer" data-url="%s"' % clip.strip()
    else:
        config['TEXT_TO_SPRITZ'] = json.dumps(clip)

    return render_template('spritz_flask.html', **config)
