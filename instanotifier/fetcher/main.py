from instanotifier.fetcher.rss.fetcher import fetch_rss_feed


def fetch(url):
    # TODO: Determining that a feed is password-protected
    # TODO: if source_id:
    #   specify the Etag and Last-Modified values.
    # * update source_entry_status when the permanently deleted status received

    result = fetch_rss_feed(url)

    # TODO: check feed.status and consider the permanent redirect
    # TODO: FeedParser object has a lot of unnecessary fields, do we need to pass them
    # to parser?

    return result
