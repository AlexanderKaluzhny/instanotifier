from __future__ import unicode_literals

from django.db import models
from django_celery_beat.models import IntervalSchedule
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class FeedSource(models.Model):
    url = models.URLField(blank=False)
    email_to = models.CharField(max_length=255, blank=False)
    interval = models.ForeignKey(IntervalSchedule)
    enabled = models.BooleanField(default=True, blank=False)


    def __str__(self):
        return u'%s - %s - %s' % (self.url[:40], self.interval, self.email_to[:40])
