from instanotifier.fetcher.tasks import fetch
from instanotifier.fetcher.rss.fetcher import fetch_rss_feed


def fetch_rss_url_in_process(url):
    result = fetch_rss_feed(url)
    return result


def fetch_url_through_task(url):
    result = fetch.delay(url).get()
    return result
