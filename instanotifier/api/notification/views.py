from django.db.models.functions import Trunc
from django.db.models import DateField, Count
from django.db.models.expressions import F

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListAPIView
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, TemplateHTMLRenderer

from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from instanotifier.api.serializers import RssNotificationSerializer, RssNotificationDateSerializer
from instanotifier.notification.models import RssNotification


class TemplateHTMLRendererBase(TemplateHTMLRenderer):
    """ Base class that converts the context into a dict """

    def _convert_context_into_dict(self, context):
        if not 'results' in context and not isinstance(context, dict):
            context = dict(
                results=context
            )
        return context

    def get_template_context(self, data, renderer_context):
        # NOTE: the data input argument should be a dictionary, according
        # to parent get_template_context()
        # The pagination of view translates the queryset into a dict.

        context = super(TemplateHTMLRendererBase, self).get_template_context(data, renderer_context)

        context = self._convert_context_into_dict(context)
        return context


class ListViewTemplateRenderer(TemplateHTMLRendererBase, BrowsableAPIRenderer):
    """ Renders the list of RssNotifications into an html. Supports searching. """

    template_name = 'api/notification/rssnotification_api_list.html'

    def get_template_context(self, data, renderer_context):
        view = renderer_context['view']
        request = renderer_context['request']
        response = renderer_context['response']

        context = super(ListViewTemplateRenderer, self).get_template_context(data, renderer_context)

        if getattr(view, 'paginator', None) and view.paginator.display_page_controls:
            paginator = view.paginator
        else:
            paginator = None

        context['paginator'] = paginator
        context['filter_form'] = self.get_filter_form(data, view, request)
        context['filter_date_used'] = view.filter_date_used if hasattr(view, 'filter_date_used') else ''

        return context


class PaginationSettings(PageNumberPagination):
    page_size = 10


class NotificationListView(ListAPIView):
    """ Renders list of RssNotification objects """

    queryset = RssNotification.objects.all()
    serializer_class = RssNotificationSerializer
    renderer_classes = (ListViewTemplateRenderer, JSONRenderer, BrowsableAPIRenderer,)

    pagination_class = PaginationSettings
    # permission_classes =
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ['title', 'summary']
    filter_fields = {
        'published_parsed': ['date']  # filtering datetime using the __date lookup function
    }

    def filter_queryset(self, queryset):
        qs = super(NotificationListView, self).filter_queryset(queryset)

        if 'published_parsed__date' in self.request.query_params:
            self.filter_date_used = self.request.query_params['published_parsed__date']

        return qs


class NotificationDatesListView(ListAPIView):
    """ Renders list of dates picked from the RssNotification published_parsed field. """

    template_name = 'api/notification/rssnotification_date_list.html'
    renderer_classes = (TemplateHTMLRendererBase, JSONRenderer,)
    serializer_class = RssNotificationDateSerializer

    def get_serializer(self, *args, **kwargs):
        serializer = super(NotificationDatesListView, self).get_serializer(*args, **kwargs)
        return serializer

    def get_queryset(self):
        """ Returns the queryset containing entries having the date field only.
            Date is a trunc of a published_parsed datetime field.
        """

        # NOTE: order_by influences the distinct() results here
        date_times = RssNotification.objects.annotate(
            published_parsed_date=Trunc('published_parsed', 'day', output_field=DateField()),
            plain_field=F('published_parsed')
        ).values(
            'published_parsed_date'
        ).distinct().filter(plain_field__isnull=False).order_by(
            '-published_parsed_date'
        ).annotate(dates_count=Count('published_parsed'))

        return date_times