from __future__ import absolute_import

from celery import chain, shared_task

from django.shortcuts import get_object_or_404

from instanotifier.fetcher.tasks import fetch
from instanotifier.parser.tasks import parse
from instanotifier.publisher.tasks import publish
from instanotifier.fetcher.rss.utils import _rss_file_path
from instanotifier.notification.utils.feed import delete_test_rss_feed_notifications


def test_consume_feed_task_chaining():
    """ Consume test rss feed through connected fetcher and parser and publisher tasks.
        Make sure the parser have created the RssNotification instances, and
        all the messages were sent.

        It should be run from under the django shell/script.
    """
    delete_test_rss_feed_notifications()

    task_flow = chain(fetch.s(), parse.s(), publish.s())
    task_flow.delay(_rss_file_path()).get()


def _get_chain():
    return chain(fetch.s(), parse.s(), publish.s())


@shared_task
def RSS_NOTIFICATION_CHAINING_TASK(feedsource_pk):

    from instanotifier.feedsource.models import FeedSource

    url = FeedSource.objects.values_list('url', flat=True).get(pk=feedsource_pk)
    task_flow = _get_chain()
    task_flow.delay(url)
