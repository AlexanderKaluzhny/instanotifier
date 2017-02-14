from test_plus.test import TestCase

from instanotifier.fetcher import tests
from instanotifier.parser.rss.parser import RssParser
from instanotifier.parser.rss.parser import RSS_FEED_INFO_FIELDS, RSS_FEED_ENTRY_FIELDS

from instanotifier.notification.forms import RssNotificationForm

class TestRssNotificationForm(TestCase):
    def setUp(self):
        self.feed = tests.test_fetch_url_task()
        parser = RssParser(self.feed)
        self.feed_items = parser.parse_feed_items(self.feed)

    def test_create_notification(self):
        json_feed_item = self.feed_items[0]

        form = RssNotificationForm(data=json_feed_item)
        self.assertTrue(form.is_valid())
        # NOTE: if run in task_eager mode, the self.feed was not serialized by the timeawareserializer,
        # so the RssNotification form will not be valid.


