# oauth-proxy

This proxy is designed to locally expose an oauth v1 secured endpoint without oauth. You probably don't want to expose
this endpoint on the internet but can be useful for use with logstash http poller plugin for example.

Disclaimer: This solution is not well tested and will only work with HTTP GET requests.

Base functionality requires the following environment variables to be set:

        OAUTH_PROXY_BASE_URL
        OAUTH_PROXY_CONSUMER_KEY
        OAUTH_PROXY_CONSUMER_SECRET
        OAUTH_PROXY_TOKEN
        OAUTH_PROXY_TOKEN_SECRET

The easiest way to run this proxy is probably to clone this repo, fill environment settings out in docker-compose.yml
and just run "docker-compose up"

Apart from the base functionality, this proxy can convert JSON lists of objects to named objects using one of the
object attributes as the name. This is very useful if you are going to let elasticsearch index the data for example
since elasticsearch doesn't index lists of objects well. Lets assume for example you have the following list in "data"
node of the root example:

        ...
        "data" :
            [
                {
                    "type": "temperature",
                    "value": 12
                },
                {
                    "type": "humidity",
                    "value": 40
                }
            ]
        ...

You can now use the environment variable OAUTH_PROXY_JSON_LIST_TO_MAP to supply one or many, comma-seperated rules for
converting this list to named objects. e.g.

OAUTH_PROXY_JSON_LIST_TO_MAP=data:type

Will result in the replacing the "data" element in the JSON with:

        "data" :
            {
                "temperature":
                    {
                        "value": 12
                    },
                "humidity":
                    {
                        "value": 40
                    }
            }