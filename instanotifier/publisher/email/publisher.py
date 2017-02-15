from django.template.loader import render_to_string

from django.core.mail import mail_managers

from instanotifier.notification.models import RssNotification

class RssNotificationEmailPublisher(object):

    test_email_address = 'sample@example.com'
    email_template = 'publisher/email/rss_notification_email.html'

    def __init__(self, notification_pks):
        self.notifications_pks = notification_pks

    def send_email(self, rendered_notification, notification):
        from django.utils.safestring import SafeText
        assert(isinstance(rendered_notification, SafeText))

        try:
            # TODO: send_mass_mail to send to multiple recipients

            # TODO: send_mail
            mail_managers(u'{}'.format(notification.title),
                          u'{}'.format(''),
                          fail_silently=False, html_message=rendered_notification)
        except Exception as e:
            raise e

    def render_notification(self, notification):
        rendered_content = render_to_string(self.email_template, {'notification' : notification})
        return rendered_content

    def publish(self):
        # TODO: get email address from SourceSettings
        rendered_content = ''
        queryset = RssNotification.objects.filter(pk__in=self.notifications_pks)
        for notification in queryset:
            rendered_content = self.render_notification(notification)
            self.send_email(rendered_content, notification)
            # TODO: write tests for this method
