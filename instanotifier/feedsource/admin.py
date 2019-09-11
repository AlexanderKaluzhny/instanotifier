from django.contrib import admin

from instanotifier.feedsource.models import FeedSource


@admin.register(FeedSource)
class FeedSourceAdmin(admin.ModelAdmin):
    list_display = ["name", "enabled", "email_to", "created_on", "last_modified"]
