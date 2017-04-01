#!/usr/bin/env python

"""flask_oauth_proxy.py: ."""


import os
from flask import Flask, request
from requests_oauthlib import OAuth1Session, OAuth1

app = Flask(__name__)

# Defaults
settings = {'OAUTH_PROXY_BASE_URL': 'https://github.com',
            'OAUTH_PROXY_CONSUMER_KEY': '',
            'OAUTH_PROXY_CONSUMER_SECRET': '',
            'OAUTH_PROXY_TOKEN': '',
            'OAUTH_PROXY_TOKEN_SECRET': ''}


@app.route('/<path:uri>')
def proxy(uri):

    # Override all settings with env vars if set
    for setting, value in settings.items():
        if os.environ.get(setting):
            settings[setting] = os.environ[setting]

        print ("%s: %s" % (setting, settings[setting]))

    target_url = "%s%s" % (settings['OAUTH_PROXY_BASE_URL'], uri)

    consumer_key = settings['OAUTH_PROXY_CONSUMER_KEY']
    consumer_secret = settings['OAUTH_PROXY_CONSUMER_SECRET']
    token = settings['OAUTH_PROXY_TOKEN']
    token_secret = settings['OAUTH_PROXY_TOKEN_SECRET']

    oauth_session = OAuth1Session(consumer_key,
                                  client_secret=consumer_secret,
                                  resource_owner_key=token,
                                  resource_owner_secret=token_secret)

    res = oauth_session.get(target_url, params=request.args)

    return res.text

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')