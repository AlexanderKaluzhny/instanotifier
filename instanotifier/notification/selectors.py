from django.db.models.functions import Trunc, TruncDay
from django.db.models import DateField, Count, Q
from django.db.models.expressions import F

from .models import RssNotification, Ratings


def daily_posted_ratings(date=None):
    initial_qs = RssNotification.objects.annotate(
        day_date=Trunc("published_parsed", "day", output_field=DateField()),
        plain_field=F("published_parsed"),
    )
    if date:
        initial_qs = initial_qs.filter(day_date=date)

    qs = (
        initial_qs.values("day_date")
        .distinct()
        .filter(plain_field__isnull=False)
        .order_by("-day_date")
        .annotate(total=Count("id"))
        .annotate(upvoted=Count("id", filter=Q(rating=Ratings.UPVOTED)))
        .annotate(downvoted=Count("id", filter=Q(rating=Ratings.DOWNVOTED)))
        .annotate(plain=Count("id", filter=Q(rating=Ratings.DEFAULT)))
        .annotate(bookmarked=Count("id", filter=Q(is_bookmarked=True)))
    )

    return qs


def daily_posted_totals():
    qs = (
        RssNotification.objects.annotate(
            day_date=TruncDay("published_parsed", output_field=DateField())
        )
        .values("day_date")
        .order_by("-day_date")
        .annotate(total=Count("id"))
    )
    return qs


def countries_total_posted(*, posts_since=None):
    initial_qs = RssNotification.objects.all()
    if posts_since:
        initial_qs = initial_qs.filter(published_parsed__gte=posts_since)

    qs = (
        initial_qs.values("country")
        .annotate(posts_count=Count("id"))
        .order_by("-posts_count")
    )
    return qs


def countries_daily_posted():
    qs = (
        RssNotification.objects.annotate(
            day_date=TruncDay("published_parsed", output_field=DateField())
        )
        .values("country", "day_date")
        .annotate(by_country_count=Count("id"))
        .order_by("country", "-day_date")
    )
    return qs
