import re
from rest_framework import serializers

from instanotifier.notification.models import RssNotification

RSSNOTIFICATION_DATE_OUTPUT_FORMAT = "%Y-%m-%d"


class RssNotificationSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()
    source_name = serializers.SerializerMethodField()

    class Meta:
        model = RssNotification
        fields = ["id", "title", "summary", "link", "published_parsed", "rating", "country", "source_name"]
        extra_kwargs = {"published_parsed": {"format": "%H:%M:%S %Y-%m-%d"}}

    def get_source_name(self, obj):
        name = obj.feed_source.name if obj.feed_source else ''
        return name

    def get_country(self, obj):
        regex = r'(?<=Country</b>: )(.*)'
        re_res = re.search(regex, obj.summary, re.MULTILINE)
        country = re_res.group(0) if re_res else 'Unknown'
        return country


class RssNotificationDateSerializer(serializers.Serializer):
    """ Serializer for rendering of the RssNotifications' published_parsed dates"""

    published_parsed_date = serializers.DateField(
        format=RSSNOTIFICATION_DATE_OUTPUT_FORMAT
    )
    dates_count = serializers.IntegerField()
    upvoted = serializers.IntegerField()
    downvoted = serializers.IntegerField()
    plain = serializers.IntegerField()
