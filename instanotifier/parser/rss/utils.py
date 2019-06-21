
def filter_feeditem_fields(feed, fields):
    feed_keys = feed.keys()
    if not len(feed_keys):
        raise ValueError("Empty feed specified.")

    # feed_info = itertools.ifilter(lambda (k,v): k in feed_keys, feed.items())

    filtered_feed = {field: feed[field] for field in fields if field in feed_keys}
    return filtered_feed
