from __future__ import absolute_import


def filter_feed_by_fields (feed, fields):
    feed_keys = feed.keys()
    if not len(feed_keys):
        raise ValueError("Empty feed specified.")

    # feed_info = itertools.ifilter(lambda (k,v): k in feed_keys, feed.items())

    filtered_feed = {field: feed[field] for field in fields if field in feed_keys}
    return filtered_feed


def get_test_rssfeed(feed_path=None):
    from instanotifier.fetcher.tests import test_fetch_url_task
    from instanotifier.parser.rss.parser import RssParser

    feed = test_fetch_url_task(feed_path)
    parser = RssParser(feed)

    return feed, parser

def get_test_feed_info_fields(feed_path=None):
    feed, parser = get_test_rssfeed(feed_path)

    keys = feed[parser.feed_info_key].keys()
    return keys

def get_test_feed_entries_fields(feed_path=None):
    feed, parser = get_test_rssfeed(feed_path)

    keys = feed[parser.feed_entries_key][0].keys()
    return keys
