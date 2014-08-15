from __future__ import absolute_import

import os

from celery import Celery
from celery import shared_task

from django.conf import settings

# set the default Django settings module for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bias_exposed.settings')
from analyze.models import analyze_feed

app = Celery('analyze')

# Pull celery config info from Django Settings.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@shared_task
def add(x, y):
    return x + y



@shared_task
def queueFeed(feed_name):
    return analyze_feed(feed_name)
