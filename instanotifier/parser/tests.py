from test_plus.test import TestCase

from django.test.utils import override_settings

from instanotifier.parser.rss.parser import RssParser
from instanotifier.parser.rss.parser import RSS_FEED_INFO_FIELDS, RSS_FEED_ENTRY_FIELDS
from instanotifier.parser.main import parse_and_save

from instanotifier.parser.rss.test_utils import get_test_rss_feed

from instanotifier.notification.models import RssNotification


class TestRssParser(TestCase):
    def setUp(self):
        self.raw_feed, _ = get_test_rss_feed()

    def test_parse_feed_info(self):
        parser = RssParser(self.raw_feed)
        feed_info = parser.parse_feed_info(self.raw_feed)

        # make sure we have filtered all the necessary fields
        self.assertEqual(sorted(RSS_FEED_INFO_FIELDS), sorted(feed_info.keys()))
        for key, value in feed_info.items():
            # check the content is equal to the original feed
            self.assertTrue(value is self.raw_feed["feed"][key])

    def test_parse_feed_items(self):
        parser = RssParser(self.raw_feed)
        feed_items = parser.parse_feed_items(self.raw_feed)

        # make sure we have all the entries from the original feed
        self.assertTrue(len(feed_items) == len(self.raw_feed["entries"]) > 0)

        for idx, item in enumerate(feed_items):
            # make sure we have filtered all the necessary fields
            self.assertEqual(sorted(RSS_FEED_ENTRY_FIELDS), sorted(item.keys()))

            for key, value in item.items():
                # feed entries order should be preserved
                # and item content should be equal to the original feed
                original_feed_entry = self.raw_feed["entries"][idx]
                parser._sanitize_published_parsed(original_feed_entry)

                self.assertTrue(value == original_feed_entry[key])


class TestParserTask(TestCase):
    def setUp(self):
        self.raw_feed, parser = get_test_rss_feed()
        self.feed_items = parser.parse_feed_items(self.raw_feed)

    def test_instances_save(self):
        self.assertTrue(RssNotification.objects.count() == 0)

        # make sure instances are parsed and saved
        saved_pks = parse_and_save(self.raw_feed, feed_source=None)

        expected_items_count = len(self.feed_items)
        actual_instances_saved_count = RssNotification.objects.count()

        self.assertEqual(len(saved_pks), expected_items_count)
        self.assertEqual(len(saved_pks), actual_instances_saved_count)
