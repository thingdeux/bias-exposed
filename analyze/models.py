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
    """
    Create the initial feed values in the RSS feed table
    """
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
        ["http://feeds.bbci.co.uk/news/politics/rss.xml", "BBC"]
    ]
    bulk_list = []
    for feed in RSS_FEEDS:
        bulk_list.append(FeedSource(source=feed[1], rss_feed_url=feed[0]))

    FeedSource.objects.bulk_create(bulk_list)


def create_initial_parse_rules():
    """
    Create the initial feed values in the parse rules table
    """
    PARSE_RULES = [
        ["AP", ".entry-content"],
        ["HuffingtonPost", "#mainentrycontent > p"],
        ["FoxNews", "article"],
        ["CNN", ".cnn_storypgraphtxt"],
        ["Reuters", "#articleText"],
        ["NPR", "#storytext"],
        ["NYT", "#story > p"],
        ["NBC", ".stack-l-content"],
        ["WashingtonPost", "#article-body"],
        ["TheGuardian", "#article-body-blocks"],
        ["ABC", "#innerbody > div > p"],
        ["BBC", ".story-body > p"]
    ]

    bulk_list = []
    for rule in PARSE_RULES:
        bulk_list.append(ParseRule(source=rule[0], dom_selector=rule[1]))

    ParseRule.objects.bulk_create(bulk_list)


def get_parse_rule(feed_name):
    rule = ParseRule.objects.filter(source=feed_name)
    if rule:
        return (rule[0].dom_selector)
    else:
        return None
