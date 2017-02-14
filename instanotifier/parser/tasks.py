from __future__ import absolute_import

from celery import shared_task

from instanotifier.parser.rss.parser import RssParser
from instanotifier.notification.views import create_rssnotification_instances


@shared_task
def parse(feed):
    parser = RssParser(feed)
    feed_info, feed_items = parser.parse()

    saved_pks = create_rssnotification_instances(feed_items)

    # TODO: update SourceModel based on feed_info

    # TODO: return the value in debug mode only
    return saved_pks
