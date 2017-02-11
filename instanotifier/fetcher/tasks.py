from __future__ import absolute_import

from celery import shared_task

from feedparser import parse


class RssParser(object):
    pass


class RssFetcher(object):
    parser_class = RssParser

    def __init__(self, url):
        self.url = url
        self.rss_parser = self.parser_class()

    def fetch(self):
        self.feed = parse(self.url)
        return self.feed


@shared_task
def fetch(url, source_id=None):
    # Fetcher <-> Source Settings Model
    # Fetcher <-> Parser

    # TODO: if source_id:
    #   specify the Etag and Last-Modified values.
    # * check feed.status and consider the permanent redirect
    # * update source_entry_status when the permanently deleted status received
    # * Determining that a feed is password-protected
    # ! use d.headers to check response headers

    # TODO: FeedParser object has a lot of unnecessary fields, do we need to pass them
    # to parser?

    fetcher = RssFetcher(url)
    result = fetcher.fetch()
    return result
