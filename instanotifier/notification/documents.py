from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from .models import RssNotification


@registry.register_document
class RssNotificationDocument(Document):
    class Index:
        name = 'rss'

    class Django:
        model = RssNotification

        fields = [
            'title',
            'summary',
            'published_parsed',
        ]
