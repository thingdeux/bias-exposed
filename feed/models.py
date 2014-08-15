from django.db import models
from datetime import datetime

class Story(models.Model):
    """
    A major news story. There will be one of these for many Feeds.
    """
    # Title of the major news story
    title = models.CharField(max_length=512)
    # Body of the story
    body = models.TextField(max_length="3000", default="")
    # Slug for the url of the story being analyzed
    article_slug = models.SlugField(max_length=500)
    # Url of the article
    url = models.URLField(max_length=2000)
    post_date = models.DateField(auto_now=False, default=datetime.now())

    def __unicode__(self):
        return self.title


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

    def __unicode__(self):
        return self.url

class Word(models.Model):
    """
    Words from articles
    Will make for easier manual Frequency distribution across multiple articles
    """
    # A word can be tied to many feeds
    feeds = models.ManyToManyField(Feed)
    word = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.word