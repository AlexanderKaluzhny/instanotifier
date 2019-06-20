from unittest import mock

from test_plus.test import TestCase

from django.core import mail
from django.test.utils import override_settings

from instanotifier.notification.models import RssNotification
from instanotifier.notification.tests.utils import create_rssnotifications_from_test_feed

from instanotifier.publisher.email.publisher import RssNotificationEmailPublisher
from instanotifier.publisher.tasks import publish

from instanotifier.feedsource.models import FeedSource

from instanotifier.notification.utils.feed import delete_test_rss_feed_notifications


class TestFeedSourceAutoCleanupContext(object):
    """ A context manager that creates the disabled FeedSource instance with all the related fields and
        cleanup everything on exit.
    """

    def __init__(self):
        pass

    def __enter__(self):
        delete_test_rss_feed_notifications()

        self.feedsource = FeedSource(**dict(
            url='https://www.example.com/ab/feed/topics/rss?securityToken=2casdasdvuybf',
            email_to='sampleAAA@example.com',
            enabled=False,
        ))
        self.feedsource.save()
        self.feedsource_pk = self.feedsource.pk
        return self

    def __exit__(self, exc, value, tb):
        delete_test_rss_feed_notifications()

        self.feedsource.delete()


class TestRssNotificationEmailPublisher(TestCase):
    def setUp(self):
        mail.outbox = []  # reset outbox

        self._feedsource_test_context = TestFeedSourceAutoCleanupContext()
        self._feedsource_test_context.__enter__()

        self.feedsource = self._feedsource_test_context.feedsource

        self.saved_pks = create_rssnotifications_from_test_feed()

    def tearDown(self):
        self._feedsource_test_context.__exit__(exc=None, value=None, tb=None)

    def test_render_notification(self):
        pk = self.saved_pks[0]
        publisher = RssNotificationEmailPublisher(self.saved_pks, self.feedsource.pk)

        # make sure notification is rendered
        notification = RssNotification.objects.get(pk=pk)
        rendered_content = publisher.render_notification(notification)

        self.assertIn(notification.title, rendered_content)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
    def test_send_email_mailhog(self):
        """ sends email using the smtp email backend to be received in the mailhog """

        pk = self.saved_pks[0]
        publisher = RssNotificationEmailPublisher(self.saved_pks, self.feedsource.pk)

        notification = RssNotification.objects.get(pk=pk)
        rendered_content = publisher.render_notification(notification)
        publisher.send_email(rendered_content, notification)

    def test_send_email_local(self):
        # make sure email is sent

        pk = self.saved_pks[0]
        publisher = RssNotificationEmailPublisher(self.saved_pks, self.feedsource.pk)

        notification = RssNotification.objects.get(pk=pk)
        rendered_content = publisher.render_notification(notification)
        publisher.send_email(rendered_content, notification)
        self.assertEqual(len(mail.outbox), 1)

    # @override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
    def test_publish(self):
        # makes sure multiple emails are sent

        mail.outbox = []  # reset outbox
        publisher = RssNotificationEmailPublisher(self.saved_pks, self.feedsource.pk)
        publisher.publish()
        self.assertEqual(len(mail.outbox), len(self.saved_pks))


class TestPublishTask(TestCase):
    def setUp(self):
        self._feedsource_test_context = TestFeedSourceAutoCleanupContext()
        self._feedsource_test_context.__enter__()

        self.feedsource = self._feedsource_test_context.feedsource

        self.saved_pks = create_rssnotifications_from_test_feed()
        assert (len(self.saved_pks) > 0)

    def tearDown(self):
        self._feedsource_test_context.__exit__(exc=None, value=None, tb=None)

    @mock.patch('instanotifier.publisher.tasks.RssNotificationEmailPublisher.publish')
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_publish_task(self, publish_method_mock):
        publish.delay(self.saved_pks, self.feedsource.pk).get()
        publish_method_mock.assert_called()


def test_consume_feed_task_chaining():
    """ Consume test rss feed through connected fetcher and parser and publisher tasks.
        Make sure the parser have created the RssNotification instances, and
        all the messages were sent.

        It should be run from under the shell/script.
    """

    from celery import chain
    from instanotifier.fetcher.tasks import fetch
    from instanotifier.parser.tasks import parse
    from instanotifier.fetcher.rss.utils import _rss_file_path

    with TestFeedSourceAutoCleanupContext() as context:
        original_notification_count = RssNotification.objects.count()
        print('Original notifications count: %s' % (original_notification_count)

        task_flow = chain(fetch.s(_rss_file_path()), parse.s(), publish.s(context.feedsource_pk))
        task_flow.delay().get()

        actual_notification_count = RssNotification.objects.count()
        print('Actual notifications count: %s' % (actual_notification_count))

        assert (actual_notification_count > original_notification_count)
