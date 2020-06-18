from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response

from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import MultiMatchSearchFilterBackend
from django_elasticsearch_dsl_drf.constants import MATCHING_OPTION_SHOULD

from instanotifier.notification.documents import RssNotificationDocument
from instanotifier.notification.models import RssNotification

"""
Search query constructed by the SearchViewSet
{
    "query": {
        "bool": {
            "should": [
                {
                    "multi_match": {
                        "query": "python django",
                        "fields": ["title", "summary"],
                        "operator": "and",
                        "type": "cross_fields",
                        "minimum_should_match": "100%",
                    }
                }
            ]
        }
    },
    "sort": [{"published_parsed": {"order": "desc"}}, "_score"],
    "size": 500,
    "from": 0,
}
"""

class CustomMultiMatchSearchFilterBackend(MultiMatchSearchFilterBackend):
    search_param = "search"
    matching = MATCHING_OPTION_SHOULD

    def should_search(self, request):
        search_terms = self.get_search_query_params(request)
        return bool(search_terms)


class NotificationSearchViewSet(DocumentViewSet):
    """ Endpoint to be used for searching through ElasticSearch """

    document = RssNotificationDocument
    queryset = RssNotification.objects.all()

    renderer_classes = (JSONRenderer,)

    filter_backends = (CustomMultiMatchSearchFilterBackend,)
    multi_match_search_fields = ["title", "summary"]
    multi_match_options = {
        "operator": "and",
        "type": "cross_fields",
        "minimum_should_match": "100%",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # override the search object with the django_elasticsearch_dsl implementation in order to provide
        # the Search.to_queryset() method
        self.search = self.document.search(using=self.client, index=self.index)

    def _should_search(self):
        do_search = False
        for es_filter_backend in list(self.filter_backends):
            if es_filter_backend().should_search(self.request):
                do_search = True
        return do_search

    def filter_queryset(self, queryset):
        """
        :param queryset: of type django_elasticsearch_dsl.search.Search
        :return: django_elasticsearch_dsl.search.Search object
        """
        es_query = super().filter_queryset(queryset)
        es_query = es_query.extra(from_=0, size=500).sort("-published_parsed", "_score")
        queryset = es_query

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Shows the ES raw search result
        """
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset.execute()
        return Response(data.to_dict())
