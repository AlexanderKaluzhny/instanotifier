from instanotifier.fetcher.tests import test_fetch_url


def get_item_field(feed_items, item_idx, field_name):

    if not len(feed_items) or not isinstance(feed_items, list):
        raise ValueError("Invalid feed specified.")

    item = feed_items[item_idx]

    try:
        value = item[field_name]
    except KeyError:
        raise KeyError("No key %s in %s." % (field_name, item.keys()))

    return value

def get_test_feed_item_field(item_idx, field_name, feed_path=None):
    from instanotifier.fetcher.tests import test_fetch_url
    from instanotifier.parser.rss.parser import RssParser

    feed = test_fetch_url(feed_path)

    parser = RssParser(feed)
    feed_items = parser.parse_feed_items(feed)

    return get_item_field(feed_items, item_idx, field_name)
