from django.db import models


class FeedSourceQuerySet(models.QuerySet):
    def enabled(self):
        return self.filter(enabled=True)


class FeedSource(models.Model):
    name = models.CharField(max_length=64)
    url = models.URLField(max_length=2083)
    email_to = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)

    notes = models.TextField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    objects = FeedSourceQuerySet.as_manager()

    def __str__(self):
        return f"{self.name} - {self.email_to[:40]}"
