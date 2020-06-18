from copy import deepcopy
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


class RssNotificationCreateSerializer(serializers.ModelSerializer):
    """
    Creates the RssNotification from the data provided by Feed parser.
    Evaluates the necessary fields deriving it from the data.
    """
    class Meta:
        model = RssNotification
        fields = ["entry_id", "title", "summary", "link", "published_parsed", "country", "internal_id"]

    def to_internal_value(self, data):
        new_data = deepcopy(data)
        new_data['entry_id'] = data['id']
        new_data['country'] = 'TBD'  # it is a derived field, we will set it based on "summary" field
        new_data['internal_id'] = 'TBD'  # it is a derived field, we will set it based on "entry_id" field
        new_data = super().to_internal_value(new_data)
        return new_data

    def validate_summary(self, value):
        summary = html.clean_html(value)
        return summary

    def validate(self, validated_data):
        summary = validated_data["summary"]
        validated_data["country"] = _parse_country(summary)
        validated_data["internal_id"] = _compute_entry_id_hash(validated_data["entry_id"])
        return validated_data


class RssNotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RssNotification
        fields = ["entry_id", "title", "summary", "link", "published_parsed", "country", "internal_id"]
