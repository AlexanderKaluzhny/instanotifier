from __future__ import absolute_import

from celery import shared_task
from instanotifier.fetcher.rss.fetcher import RssFetcher, fetch_rss_feed

@shared_task
def fetch(url, source_id=None):
    # Fetcher <-> Source Settings Model
    # Fetcher < - JSON - > Parser
    # TODO: Determining that a feed is password-protected

    # TODO: if source_id:
    #   specify the Etag and Last-Modified values.
    # * update source_entry_status when the permanently deleted status received

    result = fetch_rss_feed(url)
    # TODO: check feed.status and consider the permanent redirect

    # TODO: FeedParser object has a lot of unnecessary fields, do we need to pass them
    # to parser?


    return result
