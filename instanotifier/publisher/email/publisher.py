from django.template.loader import render_to_string
from django.core.mail import mail_managers, send_mail
from django.conf import settings

from instanotifier.notification.models import RssNotification
from instanotifier.feedsource.models import FeedSource


class RssNotificationEmailPublisher(object):
    """ Publisher that retrieves the RssNotifications by passed pks and emails them on the
        email specified in the FeedSource.
    """
    email_template = 'publisher/email/rss_notification_email.html'

    def __init__(self, notification_pks, feedsource_pk):
        self.notifications_pks = notification_pks
        # TODO: use only confirmed emails
        # TODO: handle multiple emails
        self.email_to = FeedSource.objects.values_list('email_to', flat=True).get(pk=feedsource_pk)

    def send_email(self, rendered_notification, notification):
        from django.utils.safestring import SafeText
        assert (isinstance(rendered_notification, SafeText))

        try:
            # TODO: send_mass_mail to send to multiple recipients

            # mail_managers(u'{}'.format(notification.title),
            #               u'{}'.format(''),
            #               fail_silently=False, html_message=rendered_notification)
            send_mail('%s%s' % (settings.EMAIL_SUBJECT_PREFIX, notification.title),
                      u'{}'.format(''),
                      from_email=settings.SERVER_EMAIL,
                      recipient_list=[self.email_to, ],
                      fail_silently=False,
                      html_message=rendered_notification)

        except Exception as e:
            raise e

    def render_notification(self, notification):
        rendered_content = render_to_string(self.email_template, {'notification': notification})
        return rendered_content

    def publish(self):
        # TODO: get email address from FeedSource
        rendered_content = ''
        queryset = RssNotification.objects.filter(pk__in=self.notifications_pks)
        for notification in queryset:
            rendered_content = self.render_notification(notification)
            self.send_email(rendered_content, notification)
