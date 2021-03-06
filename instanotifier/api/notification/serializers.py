from rest_framework import serializers
from bs4 import BeautifulSoup

from instanotifier.notification.models import RssNotification

RSSNOTIFICATION_DATE_OUTPUT_FORMAT = "%Y-%m-%d"


class RssNotificationSerializer(serializers.ModelSerializer):
    source_name = serializers.SerializerMethodField()
    short_summary = serializers.SerializerMethodField()
    budget = serializers.SerializerMethodField()
    day_date = serializers.DateTimeField(source="published_parsed", format="%Y-%m-%d")

    class Meta:
        model = RssNotification
        fields = [
            "id", "title", "summary", "link", "published_parsed", "rating", "country", "source_name",
            "is_bookmarked",
            "short_summary", "budget", "day_date"
        ]
        extra_kwargs = {"published_parsed": {"format": "%H:%M:%S %Y-%m-%d"}}

    def get_source_name(self, obj):
        name = obj.feed_source.name if obj.feed_source else ''
        return name

    def get_short_summary(self, obj):
        return obj.summary[:200]

    def get_budget(self, obj):
        soup = BeautifulSoup(obj.summary)
        for budget_text in ["Budget", "Hourly Range"]:
            budget = soup.find(text=budget_text)
            if budget:
                return dict(
                    name=budget_text,
                    value=budget.find_next(string=True).strip(': \n')
                )
        return dict(name="", value="")


class RssNotificationDateSerializer(serializers.Serializer):
    """ Serializer for rendering of the RssNotifications' published_parsed dates"""

    day_date = serializers.DateField(
        format=RSSNOTIFICATION_DATE_OUTPUT_FORMAT
    )
    total = serializers.IntegerField()
    upvoted = serializers.IntegerField()
    downvoted = serializers.IntegerField()
    plain = serializers.IntegerField()




