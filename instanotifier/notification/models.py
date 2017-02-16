from __future__ import unicode_literals

import hashlib

from django.db import models
from django.utils.translation import ugettext_lazy as _

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

class RssNotification(models.Model):
    internal_id = models.CharField(_("Internal entry id"), max_length=255, db_index=True, blank=False, editable=False)

    title = models.CharField(_("Title"), max_length=255, blank=False)
    summary = models.TextField(_("Summary"), blank=True)
    link = models.URLField(_("Link"), blank=False)
    published_parsed = models.DateTimeField(_("Published"))
    entry_id = models.CharField(_("Rss entry id"), max_length=2083, blank=False)

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
