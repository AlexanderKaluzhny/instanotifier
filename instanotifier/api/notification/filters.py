from django_filters import rest_framework as filters
from django.core.validators import EMPTY_VALUES

from instanotifier.notification.models import Ratings


class RatingDownvotedFilter(filters.BooleanFilter):
    def filter(self, qs, value):
        if not value or value in EMPTY_VALUES:
            return qs

        return qs.exclude(**{self.field_name: Ratings.DOWNVOTED})


class NotificationFilter(filters.FilterSet):
    published_parsed__date = filters.DateFilter(field_name="published_parsed", lookup_expr="date")
    exclude_downvoted = RatingDownvotedFilter(field_name="rating")
