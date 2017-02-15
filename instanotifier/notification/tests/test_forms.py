from test_plus.test import TestCase

import instanotifier.parser.rss.utils as parser_utils
from instanotifier.notification.forms import RssNotificationForm

class TestRssNotificationForm(TestCase):
    def setUp(self):
        self.feed_items = parser_utils.get_test_rss_feed_items()

    def test_create_notification(self):
        json_feed_item = self.feed_items[0]

        form = RssNotificationForm(data=json_feed_item)
        self.assertTrue(form.is_valid())
        # NOTE: if run in task_eager mode, the feed_item was not serialized by the timeawareserializer,
        # so the RssNotification form will not be valid.


