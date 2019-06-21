import hashlib

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.db.models.functions import Trunc
from django.db.models import DateField, Count
from django.db.models.expressions import F

from instanotifier.notification.utils import html

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

    DEFAULT_READABLE = "default"
    UPVOTED_READABLE = "upvoted"
    DOWNVOTED_READABLE = "downvoted"

    @classmethod
    def as_choices(cls):
        return (
            (cls.DEFAULT, cls.DEFAULT_READABLE),
            (cls.UPVOTED, cls.UPVOTED_READABLE),
            (cls.DOWNVOTED, cls.DOWNVOTED_READABLE),
        )

    @classmethod
    def as_readables_dict(cls):
        return {v:k for k, v in cls.as_choices()}

    @classmethod
    def get_value_or_none(self, readable):
        return self.as_readables_dict().get(readable, None)


class RssNotificationQuerySet(models.QuerySet):
    def not_downvoted(self):
        return self.exclude(rating=Ratings.DOWNVOTED)

    def get_dates_only(self):
        """
        Returns the queryset containing entries having the date field only.
        Date is a trunc of a published_parsed datetime field.
        """

        # NOTE: order_by influences the distinct() results here
        date_times = (
            RssNotification.objects.annotate(
                published_parsed_date=Trunc(
                    "published_parsed", "day", output_field=DateField()
                ),
                plain_field=F("published_parsed"),
            )
            .values("published_parsed_date")
            .distinct()
            .filter(plain_field__isnull=False)
            .order_by("-published_parsed_date")
            .annotate(dates_count=Count("published_parsed"))
        )

        return date_times


class RssNotification(models.Model):
    internal_id = models.CharField(
        _("Internal entry id"),
        max_length=255,
        db_index=True,
        unique=True,
        blank=False,
        editable=False,
    )

    title = models.CharField(_("Title"), max_length=255, blank=False)
    summary = models.TextField(_("Summary"), blank=True)
    link = models.URLField(_("Link"), blank=False)
    published_parsed = models.DateTimeField(_("Published"))
    entry_id = models.CharField(_("Rss entry id"), max_length=2083, blank=False)
    rating = models.SmallIntegerField(
        choices=Ratings.as_choices(), default=Ratings.DEFAULT, null=False
    )
    created_on = models.DateTimeField("Created on", auto_now_add=True)

    objects = RssNotificationQuerySet.as_manager()

    class Meta:
        ordering = ["-published_parsed"]

    def __str__(self):
        return "%s %s" % (self.title, self.published_parsed)

    @classmethod
    def compute_entry_id_hash(cls, entry_id):
        return hashlib.md5(entry_id.encode("utf-8")).hexdigest()

    def evaluate_internal_id(self):
        if self.internal_id:
            return self.internal_id

        if not self.entry_id:
            raise ValueError("Entry_id is not specified.")

        self.internal_id = self.compute_entry_id_hash(self.entry_id)
        return self.internal_id

    def save(self, *args, **kwargs):
        self.evaluate_internal_id()

        self.summary = html.clean_html(self.summary)

        super().save(*args, **kwargs)
