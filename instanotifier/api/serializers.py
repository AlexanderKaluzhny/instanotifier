from rest_framework.serializers import ModelSerializer

from instanotifier.notification.models import RssNotification


class RssNotificationSerializer(ModelSerializer):
    class Meta:
        model = RssNotification
        fields = ['title', 'summary', 'link', 'published_parsed']
