from django.contrib import admin

from instanotifier.notification.models import RssNotification


@admin.register(RssNotification)
class RssNotificaionAdmin(admin.ModelAdmin):
    list_display = ["title", "feed_source", "published_parsed", "created_on"]
