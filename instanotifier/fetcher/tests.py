from django.conf import settings

from instanotifier.fetcher.rss.utils import fetch_url_through_task, fetch_rss_url_in_process

def _rss_file_path():
    file_path = str(settings.ROOT_DIR.path("data/samplerss.xml"))
    return file_path


def fetch_test_rss_url_through_task():
    test_file_path = _rss_file_path()
    assert len(test_file_path) > 0

    return fetch_url_through_task(test_file_path)


def fetch_test_rss_url_in_process():
    test_file_path = _rss_file_path()
    return fetch_rss_url_in_process(test_file_path)


def test_rss_fetcher_in_process():
    feed = fetch_test_rss_url_in_process()
    assert len(feed) != 0


def test_fetch_url_task():
    result = fetch_test_rss_url_through_task()
    assert len(result) > 0

    return result
