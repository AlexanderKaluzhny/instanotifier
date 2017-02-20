from __future__ import unicode_literals

from django.db import models
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django_celery_beat.admin import PeriodicTaskForm
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError

from instanotifier.taskapp.tasks import RSS_NOTIFICATION_CHAINING_TASK


@python_2_unicode_compatible
class FeedSource(models.Model):
    url = models.URLField(blank=False)
    email_to = models.CharField(max_length=255, blank=False)
    # TODO: the intervals are presaved for now
    interval = models.ForeignKey(IntervalSchedule)
    enabled = models.BooleanField(default=True, blank=False)

    periodic_task = models.ForeignKey(PeriodicTask, null=True, blank=True, editable=False)

    def task_name(self):
        name = u'%s - %s - %s' % (self.url[:40], self.interval, self.email_to[:40])
        return name[:200]

    def __str__(self):
        return self.task_name()

    def create_related_periodic_task(self, commit=False):
        if hasattr(self, '_periodic_task_validated'):
            if commit:
                self._periodic_task_validated.save()
            return self._periodic_task_validated

        new_periodic_task_data = dict(
            regtask=RSS_NOTIFICATION_CHAINING_TASK.name,
            name=self.task_name(),  # unique, max_length=200
            interval=self.interval.pk,  # IntervalSchedule, blank=True
            args=str(list()),  # self.pk,
            kwargs=str(dict()),
            enabled=False,

            queue='',  # blank=True, max_length=200,
            exchange='',  # max_length=200, blank=True,
            routing_key='',  # max_length=200, blank=True
            expires='',  # DateTimeField, blank=True, null=True
            description='',  # blank=True
        )

        form = PeriodicTaskForm(data=new_periodic_task_data)
        if form.is_valid():
            if commit:
                form.save()
            else:
                # self._periodic_task_form = form
                self._periodic_task_validated = form.instance
        else:
            # TODO: check it, should be raw dict
            raise ValidationError(form.errors)

        return form.instance

    def clean_fields(self, exclude=None):
        super(FeedSource, self).clean_fields(exclude)

        if self.periodic_task is None:
            # create and validate the PeriodicTask for this FeedSource
            # to report it as soon as possible in case it is invalid
            self.create_related_periodic_task()

    def update_periodic_task(self):
        if self.periodic_task is None:
            raise ValueError("The PeriodicTask field of FeedSource can't be updated because it is not populated.")

        self.periodic_task.enabled = self.enabled
        self.periodic_task.interval = self.interval
        self.periodic_task.args = str([self.pk, ])
        self.periodic_task.save()

    def save(self, *args, **kwargs):
        super(FeedSource, self).save(*args, **kwargs)

        if not self.periodic_task:
            try:
                periodic_task = self.create_related_periodic_task(commit=True)
            except ValidationError as e:
                raise ValueError(
                    "The %s could not be saved because the PeriodicTask didn't validate." % (
                        self._meta.object_name,
                    )
                )

            self.periodic_task = periodic_task
            super(FeedSource, self).save(*args, **kwargs)

        self.update_periodic_task()

        # def on_delete(self):
        #     # TODO: delete periodic task
        #     pass
