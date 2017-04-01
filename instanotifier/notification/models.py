from __future__ import unicode_literals

import hashlib

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text, python_2_unicode_compatible

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

@python_2_unicode_compatible
class RssNotification(models.Model):

    RATING_DEFAULT = 0
    RATING_UPVOTED = 1
    RATING_DOWNVOTED = -1

    RATING_DEFAULT_READABLE = 'default'
    RATING_UPVOTED_READABLE = 'upvoted'
    RATING_DOWNVOTED_READABLE = 'downvoted'

    RATING=(
        (RATING_DEFAULT, RATING_DEFAULT_READABLE),
        (RATING_UPVOTED, RATING_UPVOTED_READABLE),
        (RATING_DOWNVOTED, RATING_DOWNVOTED_READABLE),
    )

    RATINGS = {
        RATING_DEFAULT_READABLE: RATING_DEFAULT,
        RATING_UPVOTED_READABLE: RATING_UPVOTED,
        RATING_DOWNVOTED_READABLE: RATING_DOWNVOTED,
    }

    internal_id = models.CharField(_("Internal entry id"), max_length=255, db_index=True, blank=False, editable=False)

    title = models.CharField(_("Title"), max_length=255, blank=False)
    summary = models.TextField(_("Summary"), blank=True)
    link = models.URLField(_("Link"), blank=False)
    published_parsed = models.DateTimeField(_("Published"))
    entry_id = models.CharField(_("Rss entry id"), max_length=2083, blank=False)

    rating = models.SmallIntegerField(choices=RATING, default=RATING_DEFAULT, null=False)

    @staticmethod
    def compute_internal_id_hash(id):
        return hashlib.md5(id.encode('utf-8')).hexdigest()

    def evaluate_internal_id(self):
        if self.internal_id:
            return self.internal_id

        id = self.entry_id
        if not id:
            raise ValueError("Id is not specified.")

        self.internal_id = self.compute_internal_id_hash(id)
        return self.internal_id

    def save(self, *args, **kwargs):
        self.evaluate_internal_id()

        self.summary = html.clean_html(self.summary)

        super(RssNotification, self).save(*args, **kwargs)

    def check_existing(self):
        self.evaluate_internal_id()

        qs = RssNotification.objects.filter(internal_id=self.internal_id)
        if qs.exists():
            return True

        return False

    def __str__(self):
        return '%s %s' % (self.title, self.published_parsed)

    class Meta:
        ordering = ['-published_parsed']
