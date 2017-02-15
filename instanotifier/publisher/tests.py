from test_plus.test import TestCase

from django.core import mail
from django.test.utils import override_settings

from instanotifier.notification.models import RssNotification
from instanotifier.publisher.email.publisher import RssNotificationEmailPublisher



class TestRssNotificationEmailPublisher(TestCase):
    def setUp(self):
        mail.outbox = [] # reset outbox

        from instanotifier.parser.rss.utils import get_test_rssfeed
        from instanotifier.notification.views import create_rssnotification_instances

        feed, parser = get_test_rssfeed()
        feed_items = parser.parse_feed_items(feed)

        self.saved_pks = create_rssnotification_instances(feed_items)


    def test_render_notification(self):
        pk = self.saved_pks[0]
        publisher = RssNotificationEmailPublisher(self.saved_pks)

        notification = RssNotification.objects.get(pk=pk)
        rendered_content = publisher.render_notification(notification)

        self.assertIn(notification.title, rendered_content)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
    def test_send_email(self):
        pk = self.saved_pks[0]
        publisher = RssNotificationEmailPublisher(self.saved_pks)

        notification = RssNotification.objects.get(pk=pk)
        import pudb; pudb.set_trace()
        rendered_content = publisher.render_notification(notification)
        publisher.send_email(rendered_content, notification)
        self.assertEqual(len(mail.outbox), 1)
