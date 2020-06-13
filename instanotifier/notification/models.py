from django.db import models
from django.utils.translation import ugettext_lazy as _


"""
RSS_FEED_ENTRY_FIELDS = [
    u'title',
    u'summary',
    u'link',
    u'published_parsed',
    u'id'  # may be an url, hash it
]
"""


class Ratings(object):
    DEFAULT = 0
    UPVOTED = 1
    DOWNVOTED = -1

    @classmethod
    def as_choices(cls):
        return (
            (cls.DEFAULT, "default"),
            (cls.UPVOTED, "upvoted"),
            (cls.DOWNVOTED, "downvoted"),
        )

    @classmethod
    def as_display_dict(cls):
        return {v: k for k, v in cls.as_choices()}

    @classmethod
    def get_value_or_none(self, display_value):
        return self.as_display_dict().get(display_value, None)


class RssNotificationQuerySet(models.QuerySet):
    def not_downvoted(self):
        return self.exclude(rating=Ratings.DOWNVOTED)


class RssNotification(models.Model):
    internal_id = models.CharField(
        _("Internal entry id"),
        max_length=255,
        db_index=True,
        unique=True,
        editable=False,
    )
    feed_source = models.ForeignKey(
        "feedsource.FeedSource",
        on_delete=models.SET_NULL,
        related_name="rss_notifications",
        null=True,
    )
    title = models.CharField(_("Title"), max_length=255)
    summary = models.TextField(_("Summary"), blank=True)
    link = models.URLField(_("Link"), max_length=2083)
    published_parsed = models.DateTimeField(_("Published"))
    entry_id = models.CharField(_("Rss entry id"), max_length=2083)

    rating = models.SmallIntegerField(
        choices=Ratings.as_choices(), default=Ratings.DEFAULT
    )
    country = models.CharField(max_length=64)

    created_on = models.DateTimeField("Created on", auto_now_add=True)

    objects = RssNotificationQuerySet.as_manager()

    class Meta:
        ordering = ["-published_parsed"]

    def __str__(self):
        return "%s %s" % (self.title, self.published_parsed)
