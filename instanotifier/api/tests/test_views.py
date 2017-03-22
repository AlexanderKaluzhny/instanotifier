from test_plus.test import TestCase

from rest_framework.test import APIRequestFactory

from instanotifier.notification.tests.utils import create_rssnotifications_from_test_feed
from instanotifier.notification.models import RssNotification
from instanotifier.api.notification.views import NotificationDatesListView


factory = APIRequestFactory()

class TestNotificationDatesListView(TestCase):
    def setUp(self):
        from instanotifier.api.serializers import RSSNOTIFICATION_DATE_OUTPUT_FORMAT

        self.saved_pks = create_rssnotifications_from_test_feed()
        dates = RssNotification.objects.dates('published_parsed', 'day')
        self.dates = [date.strftime(RSSNOTIFICATION_DATE_OUTPUT_FORMAT) for date in dates]

        self.view = NotificationDatesListView.as_view()

    def test_view_output_queryset(self):
        request = factory.get('/', content_type='application/json')

        response = self.view(request)

        # make sure the dates are equal
        self.assertTrue(len(response.data) == len(self.dates))
        for obj in response.data:
            self.assertTrue(obj['published_parsed_date'] in self.dates)


class TestTemplateHTMLRendererBase(TestCase):
    pass
