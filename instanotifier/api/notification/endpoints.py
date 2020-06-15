from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from instanotifier.notification.models import RssNotification, Ratings
from instanotifier.notification import selectors

from .serializers import (
    RssNotificationSerializer,
    RssNotificationDateSerializer,
)

from .search import NotificationSearchViewSet
from .filters import NotificationFilter


class SearchMixin(object):
    def _filter_by_elasticsearch(self, queryset):
        """
        Return search results from ElasticSearch if the search params were specified
        :param queryset:
        :return: QuerySet
        """
        search_view = NotificationSearchViewSet()
        search_view.setup(self.request, *self.args, **self.kwargs)
        if search_view._should_search():
            es_query = search_view.filter_queryset(search_view.get_queryset())
            queryset = es_query.to_queryset()

        return queryset

    def filter_queryset(self, queryset):
        queryset = self._filter_by_elasticsearch(queryset)
        queryset = super().filter_queryset(queryset)

        return queryset


class PaginationSettings(PageNumberPagination):
    page_size = 20


class NotificationViewSet(SearchMixin,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          GenericViewSet):
    queryset = RssNotification.objects.all()
    serializer_class = RssNotificationSerializer
    pagination_class = PaginationSettings
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NotificationFilter

    def _get_rating_value(self):
        """ Get the rating value from the request. """
        rating = self.request.data.get("rating", None)
        if rating is None:
            raise ValidationError("The 'rating' parameter was not specified.")

        rating_value = Ratings.get_value_or_none(rating)
        if rating_value is None:
            raise ValidationError("The 'rating' parameter was incorrectly specified.")

        return rating_value

    @action(detail=True, methods=['patch'])
    def rate(self, request, pk):
        instance = self.get_object()
        rating_data = {"rating": self._get_rating_value()}

        serializer = self.get_serializer(instance, data=rating_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class NotificationDatesListEndpoint(ListAPIView):
    """
    Renders list of dates from the RssNotification published_parsed field.
    """
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer,)
    serializer_class = RssNotificationDateSerializer

    def get_queryset(self):
        """
        Returns the queryset containing entries having the date and rating stats fields.
        """
        return selectors.daily_posted_ratings()
