import logging
import os

from celery import Celery, Task
from celery import signals
from django.db import transaction

# set the default Django settings module for the 'celery' program.
# from django_celery_beat.models import PeriodicTask

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather.settings")

app = Celery('weather-apps', )

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object("django.conf:settings", namespace="CELERY")

app.config_from_object('weather.celeryconfig')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()


@signals.setup_logging.connect
def on_celery_setup_logging(**kwargs):
    from logging.config import dictConfig
    from django.conf import settings
    dictConfig(settings.LOGGING)


class TransactionAwareTask(Task):
    '''
    Task class which is aware of django db transactions and only executes tasks
    after transaction has been committed
    '''
    abstract = True

    def apply_async(self, *args, **kwargs):
        '''
        Unlike the default task in celery, this task does not return an async result
        '''
        transaction.on_commit(lambda: super(TransactionAwareTask, self).apply_async(*args, **kwargs))
