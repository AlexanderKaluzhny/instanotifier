from test_plus.test import TestCase

from instanotifier.fetcher import tests
from instanotifier.parser.rss.parser import RssParser
from instanotifier.parser.rss.parser import RSS_FEED_INFO_FIELDS, RSS_FEED_ENTRY_FIELDS


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
