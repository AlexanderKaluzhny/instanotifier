from django.shortcuts import render
from django.db.utils import IntegrityError

from instanotifier.notification.forms import RssNotificationForm


def create_rssnotification_instances(feed_items):
    saved_pks = list()
    for item in feed_items:
        form = RssNotificationForm(data=item)
        if form.is_valid():
            try:
                instance = form.save()
            except IntegrityError:
                continue
            saved_pks.append(instance.pk)

    return saved_pks
