from __future__ import absolute_import

import os

from celery import Celery
from celery import shared_task

from django.conf import settings

# set the default Django settings module for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bias_exposed.settings')
from analyze.models import analyze_feed, analyze_all_feeds

app = Celery('analyze')

# Pull celery config info from Django Settings.
app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


"""
Celery Tasks
Each task will spin off it's own celery process
"""


# Task for crawling/processing 1 RSS Feed
@shared_task
def queueFeed(feed_name):
    return analyze_feed(feed_name)


# Task for crawling/processing all RSS Feeds
@shared_task
def crawl_all_feeds():
    return analyze_all_feeds()


# Task for analyzing one feed this will check every feed item
# In the feed and try to find like items amongst the other feeds
@shared_task
def process_feed(feed_name):
    processing = True
    main_feed = queueFeed(feed_name)
    feeds = crawl_all_feeds()

    while processing:
        if feeds.ready() and main_feed.ready():
            processing = False


@shared_task
def compare_tests():
    return [queueFeed("NYT"), queueFeed("NPR"), queueFeed("FoxNews"), queueFeed('Reuters')]
