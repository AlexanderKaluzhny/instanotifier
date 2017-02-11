from __future__ import absolute_import

from celery import shared_task

from feedparser import parse


class RssFetcher(object):
    # parser_class = RssParser

    def __init__(self, url):
        self.url = url
        # self.rss_parser = self.parser_class()

    def fetch(self):
        self.feed = parse(self.url)
        return self.feed


@shared_task
def fetch(url, source_id=None):
    # Fetcher <-> Source Settings Model
    # Fetcher < - JSON - > Parser
    # TODO: Determining that a feed is password-protected

    # TODO: if source_id:
    #   specify the Etag and Last-Modified values.
    # * update source_entry_status when the permanently deleted status received

    fetcher = RssFetcher(url)
    result = fetcher.fetch()
    # TODO: check feed.status and consider the permanent redirect

    # TODO: FeedParser object has a lot of unnecessary fields, do we need to pass them
    # to parser?


    return result
