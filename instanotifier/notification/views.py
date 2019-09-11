import logging
from datetime import timedelta

from django.utils import timezone
from django.db.utils import IntegrityError

from instanotifier.notification.forms import RssNotificationForm
from instanotifier.notification.models import RssNotification


def create_rssnotification_instances(feed_items, feed_source=None):
    saved_pks = list()
    for item in feed_items:
        form = RssNotificationForm(data=item)
        if form.is_valid():
            cd = form.cleaned_data
            entry_id = cd["entry_id"]
            title = cd["title"]

            if RssNotification.objects.filter(
                title=title, created_on__gte=timezone.now() - timedelta(days=1)
            ).exists():
                logging.info(f"Skipping item `{title}` as already existing.")
                continue

            try:
                instance = form.save()
            except IntegrityError:
                logging.info(f"Skipping item `{title}` as already existing.")
                continue

            if feed_source:
                instance.feed_source = feed_source
                instance.save()

            saved_pks.append(instance.pk)

    return saved_pks
