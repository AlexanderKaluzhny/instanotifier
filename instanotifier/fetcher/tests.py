from django.conf import settings

from instanotifier.fetcher.tasks import fetch
from instanotifier.fetcher.rss.fetcher import fetch_rss_feed

def rss_file_path():
    file_path = str(settings.ROOT_DIR.path('data/samplerss.xml'))
    return file_path

def test_rss_fetcher(test_file_path=None):
    if not test_file_path:
        test_file_path = rss_file_path()

    feed = fetch_rss_feed(test_file_path)
    assert (len(feed) != 0)

    return feed


def test_fetch_url_task(test_file_path=None):
    if not test_file_path:
        test_file_path = rss_file_path()

    assert len(test_file_path) > 0

    result = fetch.delay(test_file_path)
    result = result.get()

    assert len(result) > 0
    return result

