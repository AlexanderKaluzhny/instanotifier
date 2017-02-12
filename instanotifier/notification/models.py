from __future__ import unicode_literals

import hashlib

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

class RssNotification(models.Model):
    internal_id = models.CharField(_("Internal entry id"), max_length=255, db_index=True, blank=False, editable=False)

    title = models.CharField(_("Title"), max_length=255, blank=False)
    summary = models.TextField(_("Summary"), blank=True)
    link = models.URLField(_("Link"), blank=False)
    published_parsed = models.DateTimeField(_("Published"))
    id = models.CharField(_("Rss entry id"), max_length=2083, blank=False)

    def compute_internal_id(self, id):
        if not id:
            raise ValueError("Id is not specified.")

        hash = hashlib.md5(id.encode('utf-8')).hexdigest()
        return hash

    def save(self, *args, **kwargs):
        # TODO: check self.id.encode
        self.internal_id = self.compute_internal_id(self.id)

        super(RssNotification, self).save(*args, **kwargs)
