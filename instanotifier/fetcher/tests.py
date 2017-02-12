from django.conf import settings

from instanotifier.fetcher.tasks import fetch


def rss_file_path():
    file_path = str(settings.ROOT_DIR.path('data/samplerss.xml'))
    return file_path


def test_fetch_url(test_file_path=None):
    if not test_file_path:
        test_file_path = rss_file_path()

    assert len(test_file_path) > 0

    result = fetch.delay(test_file_path)
    result = result.get()

    assert len(result) > 0
    return result
