from django.db import models


class FeedSource(models.Model):
    url = models.URLField(blank=False)
    email_to = models.CharField(max_length=255, blank=False)
    enabled = models.BooleanField(default=True, blank=False)

    def task_name(self):
        return "%s - %s" % (self.url[:40], self.email_to[:40])

    def __str__(self):
        return self.task_name()
