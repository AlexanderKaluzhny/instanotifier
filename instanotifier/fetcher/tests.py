from instanotifier.fetcher.rss import utils

def test_rss_fetcher_in_process():
    feed = utils.fetch_test_rss_url_in_process()
    assert (len(feed) != 0)

def test_fetch_url_task():

    result = utils.fetch_test_rss_url_through_task()
    assert len(result) > 0

    return result

