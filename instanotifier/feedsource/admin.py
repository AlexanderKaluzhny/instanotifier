from django.contrib import admin

from instanotifier.feedsource.models import FeedSource

@admin.register(FeedSource)
class FeedSourceAdmin(admin.ModelAdmin):
    pass
