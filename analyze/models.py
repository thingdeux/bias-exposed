from django.db import models
from feed.models import Story, Feed, Word
from rssfeed import RSSFeed


class FeedSource(models.Model):
    source = models.CharField("News Source", max_length=128, unique=True)
    rss_feed_url = models.URLField("RSS Feed URL", max_length=2000)

    def __unicode__(self):
        return self.source


class ParseRule(models.Model):
    """
    RSS Feeds link to articles that may require certain tweaks
    in order to be crawled properly (ex: DOM ID's, string strip rules)
    """
    source = models.ForeignKey(FeedSource)
    dom_selector = models.CharField("CSS Selection Query", max_length=1028)
    caused_error = models.BooleanField("Parsing Error?", default=False)

    def __unicode__(self):
        return self.source.source


def analyze_all_feeds():
    feed_container = []
    for feed in FeedSource.objects.all():
        feed_processed = RSSFeed(feed.rss_feed_url, feed.source)
        if feed_processed is not None:
            feed_container.append(feed_processed)
    return feed_container


def analyze_feed(feed_name):
    feed = FeedSource.objects.get(source=feed_name)
    if feed:
        feed_processed = RSSFeed(feed.rss_feed_url, feed.source)
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
        [FeedSource.objects.get(source="AP"), ".entry-content"],
        [FeedSource.objects.get(source="HuffingtonPost"), "#mainentrycontent > p"],
        [FeedSource.objects.get(source="FoxNews"), "article"],
        [FeedSource.objects.get(source="CNN"), ".cnn_storypgraphtxt"],
        [FeedSource.objects.get(source="Reuters"), "#articleText"],
        [FeedSource.objects.get(source="NPR"), "#storytext"],
        [FeedSource.objects.get(source="NYT"), "#story > p"],
        [FeedSource.objects.get(source="NBC"), ".stack-l-content"],
        [FeedSource.objects.get(source="WashingtonPost"), "#article-body"],
        [FeedSource.objects.get(source="TheGuardian"), "#article-body-blocks"],
        [FeedSource.objects.get(source="ABC"), "#innerbody > div > p"],
        [FeedSource.objects.get(source="BBC"), ".story-body > p"]
    ]

    bulk_list = []
    for rule in PARSE_RULES:
        bulk_list.append(ParseRule(source=rule[0], dom_selector=rule[1]))

    ParseRule.objects.bulk_create(bulk_list)


def get_parse_rule(feed_name):
    # Should only ever be one parse rule per feed.
    rule = ParseRule.objects.get(source__source=feed_name)
    if rule:
        return (rule.dom_selector)
    else:
        return None
