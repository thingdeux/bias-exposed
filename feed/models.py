from django.db import models
from datetime import datetime


class Story(models.Model):
    """
    A major news story. There will be one of these for many Feeds.
    The major story will be pulled from reuters newswire
    (as agnostic a news source as is available currently)
    """
    # Title of the major news story
    title = models.CharField(max_length=512)
    # Body of the story
    body = models.TextField(default="")
    # Slug for the url of the story being analyzed
    article_slug = models.SlugField(max_length=500)
    # Url of the article
    url = models.URLField(max_length=2000)
    post_date = models.DateField(auto_now=False, default=datetime.now())


class Feed(models.Model):
    """
    Each feed will be tied to a major story.
    There will be multiple feeds for each story,
    each coming from a different news source (ex: AP/BBC/Fox).
    """
    story = models.ForeignKey(Story)
    # Source of the news outlet
    source = models.CharField(max_length=50, db_index=True)
    # Feed Title
    title = models.CharField(max_length=512)
    # RSS Feed URL
    url = models.URLField(max_length=2000, default="")
    # Body of the story behind the RSS Feed
    body = models.TextField(default="")
    language_keys = models.charField(default="")
