from instanotifier.fetcher.rss.fetcher import fetch_rss_feed


def fetch_rss_url(url):
    result = fetch_rss_feed(url)
    return result
