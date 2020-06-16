import logging
from datetime import timedelta

from django.utils import timezone
from django.db.utils import IntegrityError

from instanotifier.notification.serializers import (
    RssNotificationCreateSerializer, RssNotificationUpdateSerializer
)
from instanotifier.notification.models import RssNotification

logger = logging.getLogger('general_file')


def _update_rssnotification(validated_data):
    vd = validated_data
    instance = RssNotification.objects.get(internal_id=vd['internal_id'])
    serializer = RssNotificationUpdateSerializer(instance, data=vd)
    serializer.is_valid(raise_exception=True)
    serializer.save()


def create_rssnotification_instances(feed_items, feed_source=None):
    created_pks = list()
    for item in feed_items:
        serializer = RssNotificationCreateSerializer(data=item)
        if serializer.is_valid(raise_exception=True):
            vd = serializer.validated_data
            title = vd["title"]

            try:
                instance = serializer.save()
            except IntegrityError:
                _update_rssnotification(validated_data=vd)
                logger.info(f"Updated item `{title}`.")
            else:
                if feed_source:
                    instance.feed_source = feed_source
                    instance.save()

                created_pks.append(instance.pk)

    return created_pks
