from elasticsearch_dsl.connections import connections

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListAPIView, GenericAPIView, get_object_or_404
from rest_framework.renderers import (
    BrowsableAPIRenderer,
    JSONRenderer,
    TemplateHTMLRenderer,
)

from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework import status

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import MultiMatchSearchFilterBackend

from django.utils.functional import cached_property

from instanotifier.api.serializers import (
    RssNotificationSerializer,
    RssNotificationDateSerializer,
)
from instanotifier.api.notification.rating import RatingManager
from instanotifier.notification.models import RssNotification, Ratings

from instanotifier.notification.documents import RssNotificationDocument


class TemplateHTMLRendererBase(TemplateHTMLRenderer):
    """ Base class that converts the context into a dict """

    def _convert_context_into_dict(self, context):
        if not "results" in context and not isinstance(context, dict):
            context = dict(results=context)
        return context

    def get_template_context(self, data, renderer_context):
        # NOTE: the data input argument should be a dictionary, according
        # to parent get_template_context()
        # The pagination of view translates the queryset into a dict.

        context = super(TemplateHTMLRendererBase, self).get_template_context(
            data, renderer_context
        )

        context = self._convert_context_into_dict(context)
        return context


class ListViewTemplateRenderer(TemplateHTMLRendererBase, BrowsableAPIRenderer):
    """ Renders the list of RssNotifications into an html. Supports searching. """

    template_name = "api/notification/rssnotification_api_list.html"

    def get_template_context(self, data, renderer_context):
        view = renderer_context["view"]
        request = renderer_context["request"]
        response = renderer_context["response"]

        context = super(ListViewTemplateRenderer, self).get_template_context(
            data, renderer_context
        )

        if getattr(view, "paginator", None) and view.paginator.display_page_controls:
            paginator = view.paginator
        else:
            paginator = None

        context["paginator"] = paginator
        context["filter_form"] = self.get_filter_form(data, view, request)
        context["filter_date_used"] = (
            view.filter_date_used if hasattr(view, "filter_date_used") else ""
        )
        context["rating_checkbox"] = view.rating_manager.checkbox
        context["rating_checkbox_is_checked"] = (
            "checked" if view.rating_manager.checkbox.is_checked else ""
        )

        return context


class PaginationSettings(PageNumberPagination):
    page_size = 50


class CustomMultiMatchSearchFilterBackend(MultiMatchSearchFilterBackend):
    search_param = 'search'

    def should_search(self, request, queryset, view):
        search_terms = self.get_search_query_params(request)
        return bool(search_terms)


class NotificationListView(ListAPIView):
    """ Renders list of RssNotification objects. Searching through the ElasticSearch """

    document = RssNotificationDocument
    queryset = RssNotification.objects.all()

    serializer_class = RssNotificationSerializer
    renderer_classes = (ListViewTemplateRenderer, JSONRenderer, BrowsableAPIRenderer)
    pagination_class = PaginationSettings

    es_filter_backends = (CustomMultiMatchSearchFilterBackend, )
    filter_backends = (DjangoFilterBackend, )
    multi_match_search_fields = ["title", "summary"]
    filter_fields = {
        "published_parsed": [
            "date"
        ],  # filtering datetime using the __date lookup function
        "rating": ["exact"],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_for_search()

    def _init_for_search(self):
        """
        Initialize attributes necessary for ES search
        """

        self.client = connections.get_connection(
            self.document._get_using()
        )
        self.index = self.document._index._name
        self.mapping = self.document._doc_type.mapping.properties.name
        self.search = self.document.search(
            using=self.client,
            index=self.index,
        )

    @cached_property
    def rating_manager(self):
        return RatingManager()

    def _filter_by_elasticsearch(self, queryset):
        """
        Return search results from ElasticSearch
        :param queryset:
        :return: QuerySet
        """
        es_query = self.search.query()
        es_query.model = self.document.Django.model

        do_search = False
        for es_filter_backend in list(self.es_filter_backends):
            esfb = es_filter_backend()
            if esfb.should_search(self.request, es_query, self):
                do_search = True
                es_query = esfb.filter_queryset(self.request, es_query, self)

        if do_search:
            es_query = es_query.extra(from_=0, size=500)
            queryset = es_query.to_queryset()

        return queryset

    def filter_queryset(self, queryset):
        queryset = self._filter_by_elasticsearch(queryset)
        queryset = super().filter_queryset(queryset)
        #
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
