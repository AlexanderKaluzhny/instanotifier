from test_plus.test import TestCase

import instanotifier.parser.rss.test_utils as parser_utils
from instanotifier.notification import services
from instanotifier.notification.serializers import RssNotificationSerializer


class TestRssNotificationServices(TestCase):
    presaved_items_count = 5

    def setUp(self):
        self.feed_items = parser_utils.get_test_rss_feed_items()
        assert len(self.feed_items) > self.presaved_items_count

        # presave some items
        for item in self.feed_items[:self.presaved_items_count]:
            serializer = RssNotificationSerializer(data=item)
            serializer.is_valid(raise_exception=True)
            serializer.save()

    def test_already_existing_items_are_skipped_during_saving(self):
        saved_pks = services.create_rssnotification_instances(self.feed_items)

        self.assertTrue(len(saved_pks) > 0)

        # check that we did not save the already saved ones
        self.assertTrue(
            len(saved_pks) == (len(self.feed_items) - self.presaved_items_count)
        )
