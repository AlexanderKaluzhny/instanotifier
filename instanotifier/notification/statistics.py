from dateutil.relativedelta import relativedelta

from django.utils import timezone

from instanotifier.notification import selectors


def list_most_active_countries_stats(months=1, limit=10):
    most_active_qs = selectors.countries_total_posted(
        posts_since=timezone.now() - relativedelta(months=months)
    ).values("country")[:limit]
    qs = selectors.countries_daily_posted().filter(country__in=most_active_qs)
    return qs
