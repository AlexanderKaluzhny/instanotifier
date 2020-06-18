from django_filters import rest_framework as filters
from django.core.validators import EMPTY_VALUES

from instanotifier.notification.models import Ratings


class RatingDownvotedFilter(filters.BooleanFilter):
    def filter(self, qs, value):
        if not value or value in EMPTY_VALUES:
            return qs

        return qs.exclude(**{self.field_name: Ratings.DOWNVOTED})


class ShowOnlyFilterBase(filters.CharFilter):
    ALLOWED_VALUES = ["all", "upvoted", "downvoted", "bookmarked"]

    def filter(self, qs, value):
        raise NotImplementedError()


class ShowOnlyFilter(ShowOnlyFilterBase):
    def filter(self, qs, value):
        if not value or value in EMPTY_VALUES:
            return qs

        if value == "all":
            return qs
        elif value == "upvoted":
            return qs.filter(rating=Ratings.UPVOTED)
        elif value == "downvoted":
            return qs.filter(rating=Ratings.DOWNVOTED)
        elif value == "bookmarked":
            return qs.filter(is_bookmarked=True)

        return qs


class NotificationFilter(filters.FilterSet):
    published_parsed__date = filters.DateFilter(field_name="published_parsed", lookup_expr="date")
    exclude_downvoted = RatingDownvotedFilter(field_name="rating")
    show_only = ShowOnlyFilter()


class DatesShowOnlyFilter(ShowOnlyFilterBase):
    """
    Based on the `daily_posted_ratings` results, filters days that have
    "upvoted", "downvoted", "bookmarked" notifications.
    """

    def filter(self, qs, value):
        if not value or value in EMPTY_VALUES:
            return qs

        if value == "all":
            return qs
        elif value == "upvoted":
            return qs.filter(upvoted__gt=0)
        elif value == "downvoted":
            return qs.filter(downvoted__gt=0)
        elif value == "bookmarked":
            return qs.filter(bookmarked__gt=0)

        return qs


class DatesFilter(filters.FilterSet):
    show_only = DatesShowOnlyFilter()
