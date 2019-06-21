import os
import logging
import stackprinter

from celery import Celery, Task
from celery.schedules import crontab

from django.apps import apps, AppConfig
from django.conf import settings

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "config.settings.local"
    )  # pragma: no cover

app = Celery("instanotifier")


class CeleryConfig(AppConfig):
    name = "instanotifier.taskapp"
    verbose_name = "Celery Config"

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        app.config_from_object("django.conf:settings", namespace="CELERY")
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)


app.conf.beat_schedule = {
    'fetch_all_sources_daily': {
        'task': 'instanotifier.feedsource.tasks.fetch_all_sources',
        'schedule': crontab(minute=00, hour=[9]),
    },
}


class LogErrorsTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        tb = stackprinter.format(exc)
        logging.error(tb)
        super().on_failure(exc, task_id, args, kwargs, einfo)


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))  # pragma: no cover
