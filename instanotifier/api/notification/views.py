from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListAPIView
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, TemplateHTMLRenderer

from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from instanotifier.api.serializers import RssNotificationSerializer
from instanotifier.notification.models import RssNotification


class ListViewTemplateRenderer(TemplateHTMLRenderer):
    template_name = 'api/notification/rssnotification_api_list.html'

    def get_template_context(self, data, renderer_context):
        view = renderer_context['view']

        context = super(ListViewTemplateRenderer, self).get_template_context(data, renderer_context)

        if getattr(view, 'paginator', None) and view.paginator.display_page_controls:
            paginator = view.paginator
        else:
            paginator = None

        context['paginator'] = paginator
        return context


class PaginationSettings(PageNumberPagination):
    page_size = 10


class NotificationListView(ListAPIView):
    queryset = RssNotification.objects.all()
    serializer_class = RssNotificationSerializer
    renderer_classes = (BrowsableAPIRenderer, ListViewTemplateRenderer, JSONRenderer,)

    pagination_class = PaginationSettings
    # permission_classes =
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title', 'summary']

    # def get_renderer_context(self):
    #     context = super(NotificationListView, self).get_renderer_context()

