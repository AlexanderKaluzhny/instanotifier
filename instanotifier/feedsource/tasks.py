from celery import chain, shared_task

from instanotifier.fetcher.main import fetch
from instanotifier.parser.main import parse
from instanotifier.publisher.tasks import publish

from instanotifier.feedsource.models import FeedSource


@shared_task
def consume_feed(url):
    fetched_feed = fetch(url)
    saved_pks = parse(feed=fetched_feed)
    return saved_pks


@shared_task
def process_feed(feedsource_pk):
    url = FeedSource.objects.values_list("url", flat=True).get(pk=feedsource_pk)

    task_flow = chain(
        consume_feed.s(url=url),
        publish.s(feedsource_pk=feedsource_pk)
    )
    task_flow.delay()


@shared_task
def fetch_all_sources():
    feedsource_pks = list(FeedSource.objects.values_list('pk', flat=True))
    for pk in feedsource_pks:
        process_feed.delay(feedsource_pk=pk)

    return {
        'fetch_started': len(feedsource_pks)
    }
