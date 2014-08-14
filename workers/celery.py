from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings


# set the default Django settings module for 'celery'
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('workers',
             broker='redisbroker',
             backend='redisbackend',
             include=['workers.tasks'])


# Celery Config parameters as a class
class Config:
    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE = "America/Los_Angeles"
    # Only run 4 threads total
    CELERYD_CONCURRENCY = 4

app.config_from_object(Config)
