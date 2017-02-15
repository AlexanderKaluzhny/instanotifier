from django.conf import settings

from instanotifier.fetcher.tasks import fetch
from instanotifier.fetcher.rss.fetcher import fetch_rss_feed

def _rss_file_path():
    file_path = str(settings.ROOT_DIR.path('data/samplerss.xml'))
    return file_path

def fetch_rss_url_in_process(url):
    result = fetch_rss_feed(url)
    return result

def fetch_url_through_task(url):
    result = fetch.delay(url).get()
    return result

def fetch_test_rss_url_through_task():
    test_file_path = _rss_file_path()
    assert(len(test_file_path) > 0)

    return fetch_url_through_task(test_file_path)

def fetch_test_rss_url_in_process():
    test_file_path = _rss_file_path()
    return fetch_rss_url_in_process(test_file_path)
