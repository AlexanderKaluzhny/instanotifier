from django.contrib import admin

from instanotifier.notification.models import RssNotification

@admin.register(RssNotification)
class RssNotificaionAdmin(admin.ModelAdmin):
    pass
