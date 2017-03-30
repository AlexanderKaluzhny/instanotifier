from rest_framework import serializers

from instanotifier.notification.models import RssNotification

RSSNOTIFICATION_DATE_OUTPUT_FORMAT = '%Y-%m-%d'


class RssNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RssNotification
        fields = ['title', 'summary', 'link', 'published_parsed', 'rating']
        extra_kwargs = {
            'published_parsed': {'format': '%H:%M:%S %Y-%m-%d'}
        }


class RssNotificationDateSerializer(serializers.Serializer):
    """ Serializer for separating the RssNotifications' published_parsed dates"""

    published_parsed_date = serializers.DateField(format=RSSNOTIFICATION_DATE_OUTPUT_FORMAT)
    dates_count = serializers.IntegerField()
