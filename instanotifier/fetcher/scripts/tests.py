from django.conf import settings

from instanotifier.fetcher.tasks import fetch


def test_fetch_url():
    rss_file_path = str(settings.ROOT_DIR.path('data/samplerss.txt'))
    result = fetch.delay(rss_file_path)
    print result.get()


def run():
    test_fetch_url()
