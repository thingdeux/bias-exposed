from __future__ import absolute_import
from feedproc import app

from .. analyze.models import analyze_feed


@app.task
def runFeed(url):
    return analyze_feed(url)

@app.task
def add(x, y):
    return x + y
