from test_plus.test import TestCase

from rest_framework.test import APIRequestFactory

from instanotifier.notification.tests.utils import (
    create_rssnotifications_from_test_feed,
)
from instanotifier.notification.models import RssNotification
from instanotifier.api.notification.views import NotificationListView

factory = APIRequestFactory()


class TestNotificationListViewFiltering(TestCase):
    def setUp(self):
        from instanotifier.api.serializers import RSSNOTIFICATION_DATE_OUTPUT_FORMAT

        self.saved_pks = create_rssnotifications_from_test_feed()
        dates = RssNotification.objects.dates("published_parsed", "day")
        self.dates = [
            date.strftime(RSSNOTIFICATION_DATE_OUTPUT_FORMAT) for date in dates
        ]

        self.view = NotificationListView.as_view()

    def test_date_filtered_is_in_response(self):
        """ Make sure the response contains the date filtered by """

        import pudb

        pudb.set_trace()

        filtering_data = {"published_parsed__date": self.dates[0]}

        request = factory.get("/", data=filtering_data, content_type="application/json")
        response = self.view(request)

        expected = '<span id="filter_date_used" data-date="{}"></span>'.format(
            self.dates[0]
        )
        self.assertTrue(expected in response.rendered_content)

    def test_date_filtered_empty_is_in_response(self):
        filtering_data = {"published_parsed__date": ""}

        request = factory.get("/", data=filtering_data, content_type="application/json")
        response = self.view(request)

        expected = '<span id="filter_date_used" data-date=""></span>'
        self.assertTrue(expected in response.rendered_content)
