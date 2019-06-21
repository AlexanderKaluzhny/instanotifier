from celery import chain

from instanotifier.notification.models import RssNotification
from instanotifier.feedsource.tasks import consume_feed
from instanotifier.publisher.tasks import publish

from instanotifier.fetcher.tests import _rss_file_path


def test_consume_feed():
    """
    It should be run from under the shell/script.

    Consume test rss feed through connected fetcher and parser tasks.
    And make sure the parser have created the RssNotification instances.
    """
    original_notification_count = RssNotification.objects.count()
    print('Original notifications count: %s' % (original_notification_count))

    test_url = _rss_file_path()
    saved_pks = consume_feed.s(url=test_url).delay().get()

    actual_notification_count = RssNotification.objects.count()
    print('Actual notifications count: %s' % (actual_notification_count))

    print('Number of saved notifications: %s' % (len(saved_pks)))
    assert (len(saved_pks) == actual_notification_count - original_notification_count)


def test_consume_and_publish():
    """
    It should be run from under the shell/script.

    Consumes test rss feed through connected fetcher and parser and publisher tasks.
    Make sure the parser have created the RssNotification instances, and
    all the messages were sent.
    """
    from instanotifier.publisher.tests import TestFeedSourceAutoCleanupContext

    with TestFeedSourceAutoCleanupContext() as context:
        original_notification_count = RssNotification.objects.count()
        print('Original notifications count: %s' % (original_notification_count))

        task_flow = chain(
            consume_feed.s(url=_rss_file_path()),
            publish.s(feedsource_pk=context.feedsource_pk)
        )
        task_flow.delay().get()

        actual_notification_count = RssNotification.objects.count()
        print('Actual notifications count: %s' % (actual_notification_count))

        assert (actual_notification_count > original_notification_count)
