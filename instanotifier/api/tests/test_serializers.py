from test_plus.test import TestCase

import instanotifier.parser.rss.utils as parser_utils

from instanotifier.notification.models import RssNotification
from instanotifier.notification.tests.utils import create_rssnotifications_from_test_feed

from instanotifier.api.serializers import RssNotificationSerializer


class TestRssNotificationSerializer(TestCase):
    def setUp(self):
        self.feed_items = parser_utils.get_test_rss_feed_items()

        self.saved_pks = create_rssnotifications_from_test_feed()
        self.notification_instance = RssNotification.objects.first()

    def test_serializer(self):
        """ make sure serializer works properly """

        json_feed_item = self.feed_items[0]

        serializer = RssNotificationSerializer(data=json_feed_item)
        self.assertTrue(serializer.is_valid())
