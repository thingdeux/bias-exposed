from django.db import models
from datetime import datetime


class Story(models.Model):
    """
    A major news story. There will be one of these to many Articles.
    """
    # Title of the major news story
    title = models.TextField(max_length=1024)
    # Tagline for the story
    tag = models.TextField(max_length=512, default="")
    # Slug for the url of the story
    article_slug = models.SlugField(max_length=1400)
    isPublished = models.BooleanField("Story Active?", default=False)
    published_date = models.DateField(auto_now=True)
    # | Seperated list of shared words between articles
    shared_words = models.CharField(max_length=4000, default="")

    def __unicode__(self):
        return self.title


class Word(models.Model):
    """
    Unique words from articles, many words can be tied to
    one article.
    """
    word = models.CharField(max_length=512, unique=True)

    def __unicode__(self):
        return self.word


class Article(models.Model):
    """
    Each Article will be tied to a major story.
    There will be multiple feeds for each story,
    each coming from a different news source (ex: AP/BBC/Fox).
    """
    story = models.ForeignKey(Story)
    # Source of the news outlet
    source = models.CharField("Article Source", max_length=50)
    # Feed Title
    title = models.CharField("Title", max_length=512)
    # Article feed URL
    url = models.URLField("URL", max_length=2000)
    # Many words from
    words = models.ManyToManyField(Word, through='Detail')
    # Whether or not the article is neutral, seemingly negative or
    # Seemingly positive about this particular topic.
    MOOD_SELECTION = {
        ('VERY_POSITIVE', "Very Positive"),
        ('POSITIVE', "Positive"),
        ('NEUTRAL', "Neutral"),
        ('NEGATIVE', "Negative"),
        ('VERY_NEGATIVE', "Very Negative"),
    }
    mood = models.CharField(max_length=30, choices=MOOD_SELECTION,
                            db_index=True, default="NEUTRAL")

    def __unicode__(self):
        return (self.source + u": " + self.title[:10])


class Detail(models.Model):
    word = models.ForeignKey(Word)
    article = models.ForeignKey(Article)
    usage = models.PositiveIntegerField(default=1)
