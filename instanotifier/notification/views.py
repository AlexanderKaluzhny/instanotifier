from django.shortcuts import render

from instanotifier.notification.forms import RssNotificationForm


def create_rssnotification_instances(feed_items):
    saved_pks = list()
    for item in feed_items:
        form = RssNotificationForm(data=item)
        if form.is_valid() and not form.instance.check_existing():
            instance = form.save()
            saved_pks.append(instance.pk)

    return saved_pks
