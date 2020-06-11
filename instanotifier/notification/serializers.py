import hashlib
from bs4 import BeautifulSoup

from rest_framework import serializers

from instanotifier.notification.models import RssNotification
from instanotifier.notification.utils import html


def _parse_country(summary):
    soup = BeautifulSoup(summary, features="html5lib")
    country_tag = soup.find(text="Country")
    if country_tag:
        country = country_tag.find_next(string=True).strip(': \n')
        return country
    return "Unknown"


def _compute_entry_id_hash(entry_id):
    return hashlib.md5(entry_id.encode("utf-8")).hexdigest()


class RssNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RssNotification
        fields = ["entry_id", "title", "summary", "link", "published_parsed", "country", "internal_id"]

    def to_internal_value(self, data):
        data['entry_id'] = data['id']
        data['country'] = 'TBD'  # it is a derived field, we will set it based on "summary" field
        data['internal_id'] = 'TBD'  # it is a derived field, we will set it based on "entry_id" field
        data = super().to_internal_value(data)
        return data

    def validate_summary(self, value):
        summary = html.clean_html(value)
        return summary

    def validate(self, validated_data):
        summary = validated_data["summary"]
        validated_data["country"] = _parse_country(summary)
        validated_data["internal_id"] = _compute_entry_id_hash(validated_data["entry_id"])
        return validated_data
