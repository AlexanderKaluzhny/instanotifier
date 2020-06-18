from copy import deepcopy
from test_plus.test import TestCase
from django.test.testcases import TransactionTestCase

import instanotifier.parser.rss.test_utils as parser_utils

from instanotifier.notification import services
from instanotifier.notification.models import RssNotification
from instanotifier.notification.serializers import RssNotificationCreateSerializer


class TestRssNotificationServices(TransactionTestCase):
    presaved_items_count = 5

    def setUp(self):
        self.feed_items = parser_utils.get_test_rss_feed_items()
        assert len(self.feed_items) > self.presaved_items_count

        # presave some items
        self.presaved_instances = []
        for item in self.feed_items[:self.presaved_items_count]:
            serializer = RssNotificationCreateSerializer(data=item)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            self.presaved_instances.append(instance)

    def test_items_created(self):
        created_pks = services.create_rssnotification_instances(self.feed_items)

        self.assertTrue(len(created_pks) > 0)
        self.assertTrue(
            len(created_pks) == (len(self.feed_items) - self.presaved_items_count)
        )

    def test_already_existing_items_are_updated_during_saving(self):
        modified_feed_items = deepcopy(self.feed_items)
        for item in modified_feed_items:
            item['summary'] = "modified summary"

        services.create_rssnotification_instances(modified_feed_items)

        for presaved_instance in self.presaved_instances:
            refreshed = RssNotification.objects.get(internal_id=presaved_instance.internal_id)
            self.assertNotEqual(refreshed.summary, presaved_instance.summary)
