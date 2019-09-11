import json
from django.core.serializers.json import DjangoJSONEncoder

from instanotifier.fetcher.rss.fetcher import fetch_rss_feed


def fetch_rss_url(url):
    result = fetch_rss_feed(url)
    return result


def write_to_file(filename, data):
    json_data = json.dumps(data, cls=DjangoJSONEncoder)

    with open(filename, "w") as f:
        f.write(json_data)


def read_from_file(filename):
    # NOTE: on loading the RssNotification, json.loads deserializes the publisher_parsed field into invalid format
    with open(filename, "r") as f:
        filedata = f.read()

    json_data = json.loads(filedata)
    return json_data
