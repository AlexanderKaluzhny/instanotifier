from test_plus.test import TestCase

from django.test.utils import override_settings

from instanotifier.fetcher import tests
from instanotifier.parser.rss.parser import RssParser
from instanotifier.parser.rss.parser import RSS_FEED_INFO_FIELDS, RSS_FEED_ENTRY_FIELDS

from instanotifier.parser import tasks
from instanotifier.notification.models import RssNotification


class TestRssParser(TestCase):
    def setUp(self):
        self.feed = tests.test_fetch_url()

    def test_parse_feed_info(self):
        parser = RssParser(self.feed)
        feed_info = parser.parse_feed_info(self.feed)

        # make sure we have filtered all the necessary fields
        self.assertEqual(sorted(RSS_FEED_INFO_FIELDS), sorted(feed_info.keys()))
        for key, value in feed_info.items():
            # check the content is equal to the original feed
            self.assertTrue(value is self.feed['feed'][key])

    def test_parse_feed_items(self):
        parser = RssParser(self.feed)
        feed_items = parser.parse_feed_items(self.feed)

        # make sure we have all the entries from the original feed
        self.assertTrue(len(feed_items) == len(self.feed['entries']) > 0)

        for idx, item in enumerate(feed_items):
            # make sure we have filtered all the necessary fields
            self.assertEqual(sorted(RSS_FEED_ENTRY_FIELDS), sorted(item.keys()))

            for key, value in item.items():
                # items order should be preserved
                # and item content should be equal to the original feed
                original_feed_entry = self.feed['entries'][idx]
                self.assertTrue(value is original_feed_entry[key])


class TestParserTask(TestCase):
    def setUp(self):
        self.feed = tests.test_fetch_url()
        # NOTE: if run in task_eager mode, the self.feed is not serialized by the timeawareserializer,
        # so the RssNotification form will not be valid.

        self.parser = RssParser(self.feed)
        self.feed_items = self.parser.parse_feed_items(self.feed)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_instances_save(self):
        self.assertTrue(RssNotification.objects.count() == 0)

        # make sure the parser saves the instances
        saved_pks = tasks.parse(self.feed) # .delay(self.feed).get()

        expected_items_count = len(self.feed_items)
        actual_instances_saved_count = RssNotification.objects.count()

        self.assertEqual(len(saved_pks), expected_items_count)
        self.assertEqual(len(saved_pks), actual_instances_saved_count)


def test_consume_feed():
    from celery import chain
    from instanotifier.fetcher.tasks import fetch
    from instanotifier.parser.tasks import parse
    from instanotifier.fetcher.tests import rss_file_path

    original_notification_count = RssNotification.objects.count()
    print 'Original notifications count: %s' % (original_notification_count)

    task_flow = chain(fetch.s(rss_file_path()), parse.s())
    saved_pks = task_flow.delay().get()
    print 'Number of saved notifications: %s' % (len(saved_pks))
    assert (len(saved_pks) == 0)

    actual_notification_count = RssNotification.objects.count()
    print 'Actual notifications count: %s' % (actual_notification_count)
