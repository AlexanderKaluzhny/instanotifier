import logging
from celery import chain, shared_task

from instanotifier.fetcher.main import fetch
from instanotifier.parser.main import parse_and_save
from instanotifier.publisher.tasks import publish

from instanotifier.feedsource.models import FeedSource


@shared_task
def consume_feed(feedsource_pk):
    feed_source = FeedSource.objects.get(pk=feedsource_pk)

    fetched_feed = fetch(feed_source.url)
    saved_pks = parse_and_save(feed=fetched_feed, feed_source=feed_source)

    logging.info(f"Fetched {len(saved_pks)} items from `{feed_source.name}`.")
    return saved_pks


@shared_task
def process_feed(feedsource_pk):
    task_flow = chain(
        consume_feed.s(feedsource_pk=feedsource_pk),
        publish.s(feedsource_pk=feedsource_pk),
    )
    task_flow.delay()


@shared_task
def fetch_all_sources():
    feedsource_pks = list(FeedSource.objects.enabled().values_list("pk", flat=True))
    for idx, pk in enumerate(feedsource_pks):
        process_feed.apply_async(kwargs=dict(feedsource_pk=pk), countdown=idx * 60)

    return {"fetch_started": len(feedsource_pks)}
