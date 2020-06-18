from test_plus.test import TestCase

import instanotifier.parser.rss.test_utils as parser_utils
from instanotifier.notification.serializers import RssNotificationSerializer, _compute_entry_id_hash


class TestRssNotificationSerializer(TestCase):
    def setUp(self):
        self.feed_items = parser_utils.get_test_rss_feed_items()

    def test_serializer_validates_the_feed_item(self):
        json_feed_item = self.feed_items[0]

        serializer = RssNotificationSerializer(data=json_feed_item)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        # NOTE: if run in task_eager mode, the feed_item was not serialized by the timeawareserializer,
        # so the RssNotification form will not be valid.

    def test_summary_field_is_sanitized(self):
        invalid_values = ["<script> do_bad_stuff() </script>", '<a href="javascript: routine();">Click here for $100</a>']
        expected = ["&lt;script&gt; do_bad_stuff() &lt;/script&gt;", "<a>Click here for $100</a>"]

        for idx, (invalid_value, expected) in enumerate(zip(invalid_values, expected)):
            json_feed_item = self.feed_items[idx]
            json_feed_item['summary'] = invalid_value

            serializer = RssNotificationSerializer(data=json_feed_item)
            self.assertTrue(serializer.is_valid(), serializer.errors)
            notification = serializer.save()

            self.assertEqual(
                notification.summary, expected
            )

    def test_internal_id_is_evaluated(self):
        json_feed_item = self.feed_items[0]

        serializer = RssNotificationSerializer(data=json_feed_item)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        notification = serializer.save()

        hash = _compute_entry_id_hash(json_feed_item['entry_id'])
        self.assertEqual(hash, notification.internal_id)
