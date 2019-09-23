from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListAPIView, GenericAPIView, get_object_or_404
from rest_framework.renderers import (
    BrowsableAPIRenderer,
    JSONRenderer,
)

from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework import status

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import MultiMatchSearchFilterBackend

from django.utils.functional import cached_property

from instanotifier.api.notification.renderers import ListViewTemplateRenderer, TemplateHTMLRendererBase
from instanotifier.api.serializers import (
    RssNotificationSerializer,
    RssNotificationDateSerializer,
)
from instanotifier.api.notification.rating import RatingManager
from instanotifier.notification.models import RssNotification, Ratings

from instanotifier.notification.documents import RssNotificationDocument


class PaginationSettings(PageNumberPagination):
    page_size = 50


class CustomMultiMatchSearchFilterBackend(MultiMatchSearchFilterBackend):
    search_param = "search"

    def should_search(self, request):
        search_terms = self.get_search_query_params(request)
        return bool(search_terms)


class NotificationSearchViewSet(DocumentViewSet):
    """ Endpoint to be used for searching through ElasticSearch """

    document = RssNotificationDocument
    queryset = RssNotification.objects.all()

    renderer_classes = (JSONRenderer,)

    filter_backends = (CustomMultiMatchSearchFilterBackend,)
    multi_match_search_fields = ["title", "summary"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # override the search object with the django_elasticsearch_dsl implementation in order to provide
        # the Search.to_queryset() method
        self.search = self.document.search(using=self.client, index=self.index)

    def _should_search(self):
        do_search = False
        for es_filter_backend in list(self.filter_backends):
            if es_filter_backend().should_search(self.request):
                do_search = True
        return do_search

    def filter_queryset(self, queryset):
        """
        :param queryset: of type django_elasticsearch_dsl.search.Search
        :return: django_elasticsearch_dsl.search.Search object
        """
        es_query = super().filter_queryset(queryset)
        es_query = es_query.extra(from_=0, size=500).sort("-published_parsed", "_score")
        queryset = es_query

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Shows the ES raw search result
        """
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset.execute()
        return Response(data.to_dict())


class NotificationListView(ListAPIView):
    """ Renders list of RssNotification objects. Searching through the ElasticSearch """

    queryset = RssNotification.objects.all()

    serializer_class = RssNotificationSerializer
    renderer_classes = (ListViewTemplateRenderer, JSONRenderer, BrowsableAPIRenderer)
    pagination_class = PaginationSettings

    filter_backends = (DjangoFilterBackend,)
    filter_fields = {
        "published_parsed": [
            "date"
        ],  # filtering datetime using the __date lookup function
        "rating": ["exact"],
    }

    @cached_property
    def rating_manager(self):
        return RatingManager()

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

        # custom logic for excluding of downvoted RssNotifications.
        queryset = self.rating_manager.filter_queryset(self.request, queryset, self)

        if "published_parsed__date" in self.request.query_params:
            # save current date filtered to highlight it on the page
            self.filter_date_used = self.request.query_params["published_parsed__date"]

        return queryset


class NotificationDatesListView(ListAPIView):
    """ Renders list of dates picked from the RssNotification published_parsed field. """

    template_name = "api/notification/rssnotification_date_list.html"
    renderer_classes = (TemplateHTMLRendererBase, JSONRenderer)
    serializer_class = RssNotificationDateSerializer

    def get_queryset(self):
        """
        Returns the queryset containing entries having the date and rating stats fields.
        """
        date_times = RssNotification.objects.get_dates_stats()
        return date_times


class NotificationVotingView(GenericAPIView):
    """Endpoint for setting of Notification rating. """

    # TODO: allow for current user entries only
    queryset = RssNotification.objects.all()
    serializer_class = RssNotificationSerializer

    def get_object(self):
        pk = self.request.data.get("id")
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=pk)
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def _get_rating_value(self):
        """ Get the rating value from the request. """

        rating = self.request.data.get("rating", None)
        if rating is None:
            raise ValidationError("The 'rating' parameter was not specified.")

        rating_value = Ratings.get_value_or_none(rating)
        if rating_value is None:
            raise ValidationError("The 'rating' parameter was incorrectly specified.")

        return rating_value

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        rating_data = {"rating": self._get_rating_value()}

        serializer = self.get_serializer(instance, data=rating_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
