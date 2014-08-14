from __future__ import absolute_import

from workers.celery import app
from analyze.models import analyze_feed


@app.task
def checkFeed(url):
    return analyze_feed(url)
