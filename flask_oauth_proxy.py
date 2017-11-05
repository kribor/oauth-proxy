#!/usr/bin/env python

"""flask_oauth_proxy.py: ."""


import os, json
from flask import Flask, request
from requests_oauthlib import OAuth1Session, OAuth1

app = Flask(__name__)

# Defaults
settings = {'OAUTH_PROXY_BASE_URL': 'https://github.com',
            'OAUTH_PROXY_CONSUMER_KEY': '',
            'OAUTH_PROXY_CONSUMER_SECRET': '',
            'OAUTH_PROXY_TOKEN': '',
            'OAUTH_PROXY_TOKEN_SECRET': '',
            'OAUTH_PROXY_JSON_LIST_TO_MAP' : None}


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

    # Support converting JSON lists to named key maps
    if settings['OAUTH_PROXY_JSON_LIST_TO_MAP']:
        json_obj = json.loads(res.text)

        # Rule Format : <dotted-key-to-search>:<name-field>,...
        for rule in settings['OAUTH_PROXY_JSON_LIST_TO_MAP'].split(','):
            rule_list = rule.split(':')
            print('rule_list: %s' % rule_list)

            rule_key = rule_list[0]
            rule_name_key = rule_list[1]

            # Traverse to targeted object and keep parent/key references to enable replacing of the list
            dotted_to_list_of_keys = rule_key.split('.')
            target = json_obj
            parent = None
            last_key = None
            for key in dotted_to_list_of_keys:
                parent = target
                last_key = key
                target = target[key]


            list = target
            map = {}

            for item in list:

                map[item[rule_name_key]] = item
                # Remove the name field to clean up
                map[item[rule_name_key]].pop(rule_name_key)

            # Replace the list with the new map
            parent[last_key] = map
        return json.dumps(json_obj)

    return res.text

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
