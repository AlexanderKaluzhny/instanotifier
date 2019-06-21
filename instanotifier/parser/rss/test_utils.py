def get_test_rss_feed():
    from instanotifier.fetcher.tests import fetch_test_rss_url
    from instanotifier.parser.rss.parser import RssParser

    feed = fetch_test_rss_url()
    parser = RssParser(feed)

    return feed, parser


def get_test_rss_feed_items():
    raw_feed, parser = get_test_rss_feed()

    feed_items = parser.parse_feed_items(raw_feed)
    return feed_items


def get_test_feed_info_fields():
    feed, parser = get_test_rss_feed()

    keys = feed[parser.feed_info_key].keys()
    return keys


def get_test_feed_entries_fields():
    feed, parser = get_test_rss_feed()

    keys = feed[parser.feed_entries_key][0].keys()
    return keys
