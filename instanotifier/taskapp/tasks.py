from celery import chain, shared_task

from instanotifier.fetcher.tasks import fetch
from instanotifier.parser.tasks import parse
from instanotifier.publisher.tasks import publish

from instanotifier.feedsource.models import FeedSource


@shared_task
def initiate_fetching(feedsource_pk):
    url = FeedSource.objects.values_list('url', flat=True).get(pk=feedsource_pk)

    # TODO: pass feedsource_pk into fetch

    task_flow = chain(fetch.s(), parse.s(), publish.s(feedsource_pk))
    task_flow.delay(url)
