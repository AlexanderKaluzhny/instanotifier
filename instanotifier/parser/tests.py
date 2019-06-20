from test_plus.test import TestCase

from django.test.utils import override_settings

from instanotifier.parser.rss import utils
from instanotifier.parser.rss.parser import RssParser
from instanotifier.parser.rss.parser import RSS_FEED_INFO_FIELDS, RSS_FEED_ENTRY_FIELDS

from instanotifier.parser import tasks
from instanotifier.notification.models import RssNotification


class TestRssParser(TestCase):
    def setUp(self):
        self.raw_feed, _ = utils.get_test_rss_feed()

    def test_parse_feed_info(self):
        parser = RssParser(self.raw_feed)
        feed_info = parser.parse_feed_info(self.raw_feed)

        # make sure we have filtered all the necessary fields
        self.assertEqual(sorted(RSS_FEED_INFO_FIELDS), sorted(feed_info.keys()))
        for key, value in feed_info.items():
            # check the content is equal to the original feed
            self.assertTrue(value is self.raw_feed['feed'][key])

    def test_parse_feed_items(self):
        parser = RssParser(self.raw_feed)
        feed_items = parser.parse_feed_items(self.raw_feed)

        # make sure we have all the entries from the original feed
        self.assertTrue(len(feed_items) == len(self.raw_feed['entries']) > 0)

        for idx, item in enumerate(feed_items):
            # make sure we have filtered all the necessary fields
            self.assertEqual(sorted(RSS_FEED_ENTRY_FIELDS), sorted(item.keys()))

            for key, value in item.items():
                # items order should be preserved
                # and item content should be equal to the original feed
                original_feed_entry = self.raw_feed['entries'][idx]
                self.assertTrue(value is original_feed_entry[key])


class TestParserTask(TestCase):
    def setUp(self):
        self.raw_feed, parser = utils.get_test_rss_feed()
        # NOTE: if run in task_eager mode, the self.raw_feed is not serialized by the timeawareserializer,
        # so the RssNotification form will not be valid.

        self.feed_items = parser.parse_feed_items(self.raw_feed)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_instances_save(self):
        self.assertTrue(RssNotification.objects.count() == 0)

        # make sure the parser saves the instances
        saved_pks = tasks.parse(self.raw_feed)  # .delay(self.feed).get()

        expected_items_count = len(self.feed_items)
        actual_instances_saved_count = RssNotification.objects.count()

        self.assertEqual(len(saved_pks), expected_items_count)
        self.assertEqual(len(saved_pks), actual_instances_saved_count)


def test_consume_feed():
    """
    It should be run from under the shell/script.

    Consume test rss feed through connected fetcher and parser tasks.
    And make sure the parser have created the RssNotification instances.
    """

    from celery import chain
    from instanotifier.fetcher.tasks import fetch
    from instanotifier.fetcher.tests import _rss_file_path

    original_notification_count = RssNotification.objects.count()
    print('Original notifications count: %s' % (original_notification_count))

    task_flow = chain(
        fetch.s(_rss_file_path()),
        tasks.parse.s()
    )
    saved_pks = task_flow.delay().get()

    actual_notification_count = RssNotification.objects.count()
    print('Actual notifications count: %s' % (actual_notification_count))

    print('Number of saved notifications: %s' % (len(saved_pks)))
    assert (len(saved_pks) == actual_notification_count - original_notification_count)
