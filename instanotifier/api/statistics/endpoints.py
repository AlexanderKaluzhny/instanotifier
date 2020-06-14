from rest_framework.views import APIView
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response

from instanotifier.notification import selectors
from instanotifier.notification import statistics

from .serializers import (
    transform_countries_queryset, transform_daily_total_queryset
)

class CountriesDailyStatisticsEndpoint(APIView):
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer,)

    def get(self, request, *args, **kwargs):
        countries_daily_qs = statistics.list_most_active_countries_stats()

        res = transform_countries_queryset(countries_daily_qs)
        return Response(res)


class DailyTotalPostedStatisticsEndpoint(APIView):
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer,)

    def get(self, request, *args, **kwargs):
        daily_total_qs = selectors.daily_posted_totals()

        res = transform_daily_total_queryset(daily_total_qs)
        return Response(res)
