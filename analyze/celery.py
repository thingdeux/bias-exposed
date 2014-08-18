from __future__ import absolute_import

import os

from celery import Celery, chord, signature
from django.conf import settings

# set the default Django settings module for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bias_exposed.settings')
from analyze.models import analyze_feed, FeedSource

app = Celery('analyze')

# Pull celery config info from Django Settings.
app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


"""
Celery Tasks
Each task will spin off it's own celery process
"""


# Task for crawling/processing 1 RSS Feed
@app.task(time_limit=60)
def queueFeed(feed_name):
    def check_feed_integrity(feed):
        try:
            # Check to make sure there are articles in the feed
            # Before putting it through for analysis
            if len(feed.feed_items) > 2:
                return True
            else:
                # Update DB Parse Rule for invalid
                return False
        except Exception as err:
            print (feed.source + " is not a valid feed" + str(err))
            return False

    processed_feed = analyze_feed(feed_name)
    if check_feed_integrity(processed_feed):
        return processed_feed
    else:
        return None

@app.task
def check_all_feeds(allfeeds):
    for thing in allfeeds:
        try:
            print ("Analyzing: " + str(thing.source))
        except:
            print "No Dice"

    return allfeeds


@app.task
def compare_tests():
    callback = check_all_feeds.s()
    head = [queueFeed.s(feed.source) for feed in FeedSource.objects.filter(
            parserule__caused_error=False) if feed is not None]
    result = chord(head)(callback)

    return result
