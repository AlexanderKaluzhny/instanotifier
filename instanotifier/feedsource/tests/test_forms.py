import json

from test_plus.test import TestCase

from instanotifier.feedsource.models import FeedSource
from instanotifier.feedsource.forms import FeedSourceForm


class TestFeedSource(TestCase):
    def setUp(self):
        pass

    def test_validation(self):
        feed_source_data = dict(
            url="https://www.example.com/ab/feed/topics/rss?securityToken=2casdasdvuybf",
            email_to="sample@example.com",
            enabled=True,
        )

        form = FeedSourceForm(data=feed_source_data)
        self.assertTrue(form.is_valid())
