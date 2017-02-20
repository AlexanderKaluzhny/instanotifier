import json

from test_plus.test import TestCase

from instanotifier.feedsource.models import FeedSource
from instanotifier.feedsource.forms import FeedSourceForm
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class TestFeedSource(TestCase):
    def setUp(self):
        self.interval = IntervalSchedule(every=30, period='seconds')
        self.interval.save()

    def test_create_related_periodic_task__validated_then_saved(self):
        feed_source_data = dict(
            url='https://www.example.com/ab/feed/topics/rss?securityToken=2casdasdvuybf',
            email_to='sample@example.com',
            interval=self.interval,
            enabled=True,
        )

        instance = FeedSource(**feed_source_data)
        instance.create_related_periodic_task()
        # make sure PeriodicTask object was validated by not saved
        self.assertTrue(hasattr(instance, '_periodic_task_validated'))
        self.assertTrue(PeriodicTask.objects.count() == 0)
        # make sure create_related_periodic_task saves the validated PeriodicTask on commit=True
        periodictask_returned = instance.create_related_periodic_task(commit=True)
        self.assertEqual(periodictask_returned, instance._periodic_task_validated)
        self.assertEqual(PeriodicTask.objects.count(), 1)

    def test_create_related_periodic_task__saved_on_first_run(self):
        feed_source_data = dict(
            url='https://www.example.com/ab/feed/topics/rss?securityToken=2casdasdvuybf',
            email_to='sample@example.com',
            interval=self.interval,
            enabled=True,
        )

        # make sure create_related_periodic_task() creates and saves the PeriodicTask on commit=True
        instance = FeedSource(**feed_source_data)
        self.assertIsNone(getattr(instance, '_periodic_task_validated', None))
        self.assertTrue(PeriodicTask.objects.count() == 0)
        instance.create_related_periodic_task(commit=True)
        self.assertEqual(PeriodicTask.objects.count(), 1)

        # make sure PeriodicTask interval is equal to FeedSource interval and the task is not enabled.
        periodictask = PeriodicTask.objects.first()
        self.assertEqual(instance.interval, periodictask.interval)
        self.assertTrue(not periodictask.enabled)
        # the args should be empty here
        self.assertEqual(periodictask.args, '[]')

    def test_model_clean_fields(self):
        feed_source_data = dict(
            url='https://www.example.com/ab/feed/topics/rss?securityToken=2casdasdvuybf',
            email_to='sample@example.com',
            interval=self.interval,
            enabled=True,
        )

        instance = FeedSource(**feed_source_data)
        self.assertIsNone(instance.periodic_task)
        self.assertIsNone(getattr(instance, '_periodic_task_validated', None))
        # make sure periodic_task object is created and validated in clean_fields() method
        instance.clean_fields()
        self.assertTrue(hasattr(instance, '_periodic_task_validated'))

    def test_save_method(self):
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

        # make sure periodic task was created in FeedSource.save(), and all the settings are equal
        form.save()
        self.assertEqual(PeriodicTask.objects.count(), 1)

        feedsource = FeedSource.objects.first()
        periodictask = PeriodicTask.objects.first()

        self.assertEqual(feedsource.interval, periodictask.interval)
        self.assertEqual(feedsource.enabled, periodictask.enabled)
        # make sure task args are set
        args = json.loads(feedsource.periodic_task.args)
        self.assertEqual(args[0], feedsource.pk)
