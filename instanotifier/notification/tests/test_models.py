from test_plus.test import TestCase

from django.core.exceptions import ValidationError

from instanotifier.notification.models import RssNotification


class TestRssNotification(TestCase):
    def setUp(self):
        self.test_data = {
            "entry_id": "https://www.example.com/e88eb1cdaeeae6?source=rss",
            "link": "https://www.example.com/e88eb1cdaeeae6?source=rss",
            "published_parsed": "2017-02-10 12:17:50",
            "summary": u'<a href="javascript: routine();">Click here for $100</a>',  # => <a>Click here for $100</a>
            "title": "Sample rss feed entry",
        }

    def test_model_required_fields(self):
        feed_item_data = {
            "entry_id": u"",
            "link": u"",
            "published_parsed": u"",
            "summary": u"",
            "title": u"",
        }

        notification = RssNotification(**feed_item_data)
        with self.assertRaises(ValidationError) as cm:
            notification.full_clean()

        self.assertIn("entry_id", cm.exception.error_dict)
        self.assertIn("link", cm.exception.error_dict)
        self.assertIn("title", cm.exception.error_dict)
        self.assertIn("published_parsed", cm.exception.error_dict)
        self.assertTrue(len(cm.exception.error_dict) is 4)

    def test_html_clean_on_save(self):
        """ make sure the summary field is sanitized on save()"""
        notification = RssNotification(**self.test_data)
        notification.save()
        self.assertEqual(notification.summary, "<a>Click here for $100</a>")
        notification.summary = "<script> do_bad_stuff() </script>"
        notification.save()
        self.assertEqual(
            notification.summary, "&lt;script&gt; do_bad_stuff() &lt;/script&gt;"
        )

    def test_evaluate_internal_id_on_save(self):
        """ make sure the internal_id field is generated on save()"""
        assert len(self.test_data["entry_id"]) > 0
        notification = RssNotification(**self.test_data)
        notification.save()

        hash = notification.compute_entry_id_hash(notification.entry_id)
        self.assertEqual(hash, notification.internal_id)
