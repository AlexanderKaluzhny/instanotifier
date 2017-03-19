from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListAPIView
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from instanotifier.api.serializers import RssNotificationSerializer
from instanotifier.notification.models import RssNotification


class NotificationListView(ListAPIView):
    queryset = RssNotification.objects.all()
    serializer_class = RssNotificationSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,)
    # permission_classes =
    # filter_backends = (DjangoFilterBackend,)
    # filter_fields = ['title', 'summary']
