import feedparser

class RssFetcher(object):
    # parser_class = RssParser

    def __init__(self, url):
        self.url = url
        # self.rss_parser = self.parser_class()

    def fetch(self):
        self.feed = feedparser.parse(self.url)
        return self.feed


def fetch_rss_feed(url):
    fetcher = RssFetcher(url)
    feed = fetcher.fetch()

    return feed
