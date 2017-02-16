from test_plus.test import TestCase

import instanotifier.parser.rss.utils as parser_utils
from instanotifier.notification import views
from instanotifier.notification.forms import RssNotificationForm


class TestRssNotificationViews(TestCase):
    presaved_items_count = 5

    def setUp(self):
        self.feed_items = parser_utils.get_test_rss_feed_items()
        assert(len(self.feed_items) > self.presaved_items_count)

        # presave some items
        for idx, item in zip(range(self.presaved_items_count), self.feed_items):
            notification = RssNotificationForm(data=item)
            notification.save()

    def test_create_rssnotification_instances(self):
        """ make sure the items are saved excluding the already existing ones """

        saved_pks = views.create_rssnotification_instances(self.feed_items)
        self.assertTrue(len(saved_pks) > 0)

        # check that we did not save the already saved ones
        self.assertTrue(len(saved_pks) == (len(self.feed_items) - self.presaved_items_count))
