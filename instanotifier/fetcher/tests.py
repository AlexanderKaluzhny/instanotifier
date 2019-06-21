from django.conf import settings

from instanotifier.fetcher.rss.utils import fetch_rss_url


def _rss_file_path():
    file_path = str(settings.ROOT_DIR.path("data/samplerss.xml"))
    return file_path


def fetch_test_rss_url():
    test_file_path = _rss_file_path()
    return fetch_rss_url(test_file_path)


def test_rss_fetcher():
    feed = fetch_test_rss_url()
    assert len(feed) != 0
