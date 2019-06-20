import json

from test_plus.test import TestCase

from instanotifier.feedsource.models import FeedSource
from instanotifier.feedsource.forms import FeedSourceForm
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class TestFeedSource(TestCase):
    def setUp(self):
        self.interval = IntervalSchedule(every=30, period='seconds')
        self.interval.save()

    def test_save_method(self):
        feed_source_data = dict(
            url='https://www.example.com/ab/feed/topics/rss?securityToken=2casdasdvuybf',
            email_to='sample@example.com',
            interval=self.interval.pk,
            enabled=True,
        )

        form = FeedSourceForm(data=feed_source_data)
        self.assertTrue(form.is_valid())

        feedsource = FeedSource.objects.first()
        periodictask = PeriodicTask.objects.first()

        self.assertEqual(feedsource.enabled, periodictask.enabled)
