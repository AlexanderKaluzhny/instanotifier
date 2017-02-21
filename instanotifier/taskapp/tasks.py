from __future__ import absolute_import

from celery import chain, shared_task

from instanotifier.fetcher.tasks import fetch
from instanotifier.parser.tasks import parse
from instanotifier.publisher.tasks import publish

from instanotifier.feedsource.models import FeedSource

def _get_chain(feedsource_pk):
    return chain(fetch.s(), parse.s(), publish.s(feedsource_pk))


@shared_task
def RSS_NOTIFICATION_CHAINING_TASK(feedsource_pk):
    url = FeedSource.objects.values_list('url', flat=True).get(pk=feedsource_pk)

    task_flow = _get_chain(feedsource_pk)
    task_flow.delay(url)
