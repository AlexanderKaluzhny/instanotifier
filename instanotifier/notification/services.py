import logging
from datetime import timedelta

from django.utils import timezone
from django.db.utils import IntegrityError

from instanotifier.notification.serializers import RssNotificationSerializer
from instanotifier.notification.models import RssNotification

logger = logging.getLogger('general_file')


def create_rssnotification_instances(feed_items, feed_source=None):
    saved_pks = list()
    for item in feed_items:
        serializer = RssNotificationSerializer(data=item)
        if serializer.is_valid(raise_exception=True):
            vd = serializer.validated_data
            title = vd["title"]

            if RssNotification.objects.filter(
                title=title, created_on__gte=timezone.now() - timedelta(days=1)
            ).exists():
                logger.info(f"Skipping item `{title}` as already existing.")
                continue

            try:
                instance = serializer.save()
            except IntegrityError:
                logger.info(f"Skipping item `{title}` as already existing.")
                continue

            if feed_source:
                instance.feed_source = feed_source
                instance.save()

            saved_pks.append(instance.pk)

    return saved_pks
