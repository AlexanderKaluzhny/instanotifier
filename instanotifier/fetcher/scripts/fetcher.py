from instanotifier.fetcher import tests


def run():
    # is executed when ran with 'manage.py runscript tests'
    tests.test_rss_fetcher()
