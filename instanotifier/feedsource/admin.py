from django.contrib import admin

from instanotifier.feedsource.models import FeedSource


@admin.register(FeedSource)
class FeedSourceAdmin(admin.ModelAdmin):
    list_display = [
        'url_shortened',
        'email_to',
        'last_modified',
    ]

    def url_shortened(self, obj):
        return obj.url[:40]

