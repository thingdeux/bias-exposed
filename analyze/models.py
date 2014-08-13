from django.db import models
from feed.models import Story, Feed, Word
from rssfeed import RSSFeed


class FeedSource(models.Model):
    source = models.CharField(max_length=128)
    rss_feed_url = models.CharField(max_length=2000)


class ParseRule(models.Model):
    """
    RSS Feeds link to articles that may require certain tweaks
    in order to be crawled properly (ex: DOM ID's, string strip rules)
    """
    source = models.CharField(max_length=128)
    dom_selector = models.CharField(max_length=1028)
    caused_error = models.BooleanField(default=False)


def analyze_all_feeds():
    feed_container = []
    for feed in FeedSource.objects.all():
        feed_processed = RSSFeed(feed.rss_feed_url, feed.source)
        if feed_processed is not None:
            feed_container.append(feed_processed)
    return feed_container


def analyze_feed(feed_name):
    feed = FeedSource.objects.filter(source=feed_name)
    if feed:
        feed_processed = RSSFeed(feed[0].rss_feed_url, feed[0].source)
        if feed_processed is not None:
            return feed_processed
        else:
            return None
    else:
        return None


def create_initial_rss_feeds():
    RSS_FEEDS = [
        # Breaking PEP8 for readability
        ["http://hosted.ap.org/lineups/POLITICSHEADS.rss?SITE=AP&SECTION=HOME", "AP"],
        ["http://www.huffingtonpost.com/feeds/verticals/politics/news.xml", "HuffingtonPost"],
        ["http://feeds.foxnews.com/foxnews/politics", "FoxNews"],
        ["http://rss.cnn.com/rss/cnn_allpolitics.rss", "CNN"],
        ["http://feeds.reuters.com/Reuters/PoliticsNews?format=xml", "Reuters"],
        ["http://www.npr.org/rss/rss.php?id=1014", "NPR"],
        ["http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml", "NYT"],
        ["http://feeds.nbcnews.com/feeds/topstories", "NBC"],
        ["http://feeds.washingtonpost.com/rss/rss_election-2012", "WashingtonPost"],
        ["http://feeds.theguardian.com/theguardian/politics/rss", "TheGuardian"],
        ["http://feeds.abcnews.com/abcnews/politicsheadlines", "ABC"],
        ["http://feeds.bbci.co.uk/news/politics/rss.xml", "BCC"],
        ["http://online.wsj.com/xml/rss/3_7085.xml", "WSJ"]
    ]

    for feed in RSS_FEEDS:
        new_feed = FeedSource(source=feed[1], rss_feed_url=feed[0])
        new_feed.save()
