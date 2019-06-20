from test_plus.test import TestCase

from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from django.utils.http import urlencode

from instanotifier.api.notification.views import NotificationListView
from instanotifier.api.notification.rating import (
    CheckboxExcludeDownvotedNotification,
    RatingManager,
)

from instanotifier.notification.tests.utils import (
    create_rssnotifications_from_test_feed,
)
from instanotifier.notification.models import RssNotification


factory = APIRequestFactory()


def create_view_GET_request(query_params):
    query_params_encoded = urlencode(query_params)
    request = Request(factory.get("/", query_params))
    view = NotificationListView
    view.request = request
    return view, query_params_encoded


class TestCheckboxExcludeDownvotedNotification(TestCase):
    def setUp(self):
        query_params = {"date": "2017-04-08", "someparam": "somevalue"}
        self.view, self.query_params = create_view_GET_request(query_params)

    def test_build_url__excluding_downvoted(self):
        checkbox = CheckboxExcludeDownvotedNotification()
        url = checkbox.build_url(self.view, include_all=False)
        self.assertFalse("include_rating" in url)
        # make sure other params are preserved
        self.assertTrue(self.query_params in url)

        # make sure the include_rating param is removed from query_params
        request = Request(factory.get("/", dict(include_rating="all")))
        view = NotificationListView
        view.request = request
        url = checkbox.build_url(view, include_all=False)
        self.assertFalse("include_rating" in url)

    def test_build_url__including_downvoted(self):
        checkbox = CheckboxExcludeDownvotedNotification()
        url = checkbox.build_url(self.view, include_all=True)
        self.assertTrue("include_rating" in url)
        # make sure other params are preserved
        self.assertTrue(self.query_params in url)

    def test_build_url__page_param_removed(self):
        # make sure the 'page' query param is removed when we build the url

        query_params = {"date": "2017-04-08", "someparam": "somevalue", "page": 3}
        view, query_params_encoded = create_view_GET_request(query_params)

        checkbox = CheckboxExcludeDownvotedNotification()
        url = checkbox.build_url(view, include_all=False)
        self.assertFalse(view.pagination_class.page_query_param in url)

        url = checkbox.build_url(view, include_all=True)
        self.assertFalse(view.pagination_class.page_query_param in url)
        self.assertTrue("include_rating" in url)

    def test_set_checked(self):
        checkbox = CheckboxExcludeDownvotedNotification()

        with self.assertRaises(Exception):
            # make sure it raises exception when attribute is requested before being set.
            checkbox.is_checked()

        checkbox.set_checked(True, self.view)
        self.assertTrue(checkbox.is_checked)
        self.assertTrue("include_rating" in checkbox.url)

        checkbox.set_checked(False, self.view)
        self.assertFalse(checkbox.is_checked)
        self.assertTrue("include_rating" not in checkbox.url)


class TestRatingManagerFiltering(TestCase):
    def setUp(self):

        self.saved_pks = create_rssnotifications_from_test_feed()
        queryset_downvoted = RssNotification.objects.filter(pk__in=self.saved_pks[-3:])
        queryset_downvoted.update(rating=-1)
        self.downvoted_pks = queryset_downvoted.values_list("pk", flat=True)
        query_params = {"rating": "upvoted"}
        self.view, self.query_params = create_view_GET_request(query_params)

    def test_rating_query_param(self):
        rating_manager = RatingManager()

        query_params = {"include_rating": "all", "rating": "upvoted"}
        view, _ = create_view_GET_request(query_params)

        # make sure the RatingManager doesn't filter downvoted items when there is a 'rating' query param,
        # so the input queryset doesn't change.
        qs = RssNotification.objects.all()
        filtered_queryset = rating_manager.filter_queryset(view.request, qs, view)
        expected_len = len(self.saved_pks)
        self.assertTrue(expected_len == filtered_queryset.count())
        self.assertTrue(rating_manager.checkbox.is_shown == False)

        # make sure, the qs is not filtered when the 'include_rating' query param is set
        query_params = {"include_rating": "all"}
        view, _ = create_view_GET_request(query_params)
        filtered_queryset = rating_manager.filter_queryset(view.request, qs, view)
        expected_len = len(self.saved_pks)
        self.assertTrue(expected_len == filtered_queryset.count())
        self.assertTrue(rating_manager.checkbox.is_checked == False)

    def test_rating_filtering(self):
        # make sure the downvoted items are excluded from queryset
        rating_manager = RatingManager()
        query_params = {}
        view, _ = create_view_GET_request(query_params)
        qs = RssNotification.objects.all()
        filtered_queryset = rating_manager.filter_queryset(view.request, qs, view)
        expected_len = len(self.saved_pks) - len(self.downvoted_pks)
        self.assertTrue(expected_len == filtered_queryset.count())

        # check downvoted pks are not in the list
        qs_pks = filtered_queryset.values_list("pk", flat=True)
        self.assertTrue(len(set(qs_pks) & set(self.downvoted_pks)) == 0)
