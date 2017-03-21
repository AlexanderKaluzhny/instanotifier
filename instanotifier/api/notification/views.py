from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListAPIView
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, TemplateHTMLRenderer

from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from instanotifier.api.serializers import RssNotificationSerializer
from instanotifier.notification.models import RssNotification


class ListViewTemplateRenderer(TemplateHTMLRenderer, BrowsableAPIRenderer):
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

        return context


class PaginationSettings(PageNumberPagination):
    page_size = 10


class NotificationListView(ListAPIView):
    queryset = RssNotification.objects.all()
    serializer_class = RssNotificationSerializer
    renderer_classes = (ListViewTemplateRenderer, JSONRenderer, BrowsableAPIRenderer, )

    pagination_class = PaginationSettings
    # permission_classes =
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title', 'summary']

    # def get_renderer_context(self):
    #     context = super(NotificationListView, self).get_renderer_context()


class RssNotificationDateSerializer(object):
    """ RssNotification Date Serializer mock object """

    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset
        self.many = kwargs.get('many', False)

    @property
    def data(self):
        # TODO: return serialized value
        return dict(results=self.queryset)



class NotificationDatesListView(ListAPIView):
    template_name = 'api/notification/rssnotification_date_list.html'
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer,)
    serializer_class = RssNotificationDateSerializer

    def get_serializer(self, queryset, many):
        serializer = super(NotificationDatesListView, self).get_serializer(queryset, many)
        return serializer

    def get_queryset(self):
        date_times = RssNotification.objects.values_list('published_parsed', flat=True)
        return date_times
