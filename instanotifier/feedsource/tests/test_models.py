from test_plus.test import TestCase

from instanotifier.feedsource.models import FeedSource
from instanotifier.feedsource.forms import FeedSourceForm
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class TestFeedSource(TestCase):
    def setUp(self):
        self.interval = IntervalSchedule(every=30, period='seconds')
        self.interval.save()

    def test_create_related_periodic_task(self):
        feed_source_data = dict(
            url='https://www.example.com/ab/feed/topics/rss?securityToken=2casdasdvuybf',
            email_to='sample@example.com',
            interval=self.interval.pk,
            enabled=True,
        )

        self.assertEqual(PeriodicTask.objects.count(), 0)

        form = FeedSourceForm(data=feed_source_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(hasattr(form.instance, '_periodic_task_validated'))
        feed_source_instance = form.save()

        # make sure periodic task was created
        # TODO: check feed_source_instance.periodic_task.pk without form.save()
        self.assertTrue(feed_source_instance.periodic_task.pk)
        self.assertEqual(PeriodicTask.objects.count(), 1)
        # TODO: make sure the args contain the FeedSource.pk


        # feed_source_instance.create_related_periodic_task()

    def test_periodic_task_is_disabled(self):
        pass
