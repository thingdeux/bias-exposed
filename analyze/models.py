from django.db import models
from feed.models import Story, Feed, Word
from rssfeed import RSSFeed
from django.conf import settings
import redis

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


def compare_feed(main_feed, all_feeds):
    def stage_one(main_title, other_title):
        match_score = 0
        try:
            for word in main_title:
                if word in other_title:
                    match_score += 10
        except:
            pass
        return match_score

    def stage_two(main_quotes, other_quotes):
        """
        Stage one article comparison, check to see if there article
        shared quotes between the two articles
        """
        match_score = 0
        reasons = {'quotes': []}
        # Check to see if each quote in the current article is in another_feeds
        # Quote list
        try:
            for quote in main_quotes:
                if quote in other_quotes['quotes']:
                    match_score += 20
                    reasons['quotes'].append(quote)
        except:
            pass

        if len(reasons['quotes']) >= 1:
            print ("\tQuote match")
            for line in reasons['quotes']:
                print "\t\t" + line
        return match_score

    def stage_three(main_sentences, other_sentences):
        match_score = 0
        reasons = {'sentences': []}
        try:
            for main_sentence in main_sentences:
                # Make sure the sentence is at least 3 words long
                # Should catch false positives like 'Gen.' or 'Sen.'
                if len(main_sentence.split(' ')) > 3:
                    if main_sentence in other_sentences:
                        match_score += 6
                        reasons['sentences'].append(main_sentence)
        except:
            pass
        if len(reasons['sentences']) >= 1:
            print ("\tSentences match")
            for line in reasons['sentences']:
                print "\t\t" + line
        return match_score

    def stage_four(main_body_tokens, other_body_tokens):
        match_score = 0
        try:
            for token in main_body_tokens:
                if token in other_body_tokens:
                    match_score += 1
        except:
            pass
        return match_score

    match_table = {}

    # Iterate over the main_feeds articles one at a time
    for main_feed_item in main_feed.feed_items:
        print ("[" + main_feed.source + "]" + "Checking: " + main_feed_item['title'])
        # Iterate over each RSSFeed Object in the all_feeds list
        for rss_feed in all_feeds:
            # Make sure to skip the RSSFeed Obj that equals main_feed
            if main_feed.source is not rss_feed.source:
                for other_feed_item in rss_feed.feed_items:
                    final_match_score = 0
                    try:
                        final_match_score = stage_one(
                            main_feed_item['tokenized_title'], other_feed_item['tokenized_title'])
                    except:
                        pass

                    try:
                        final_match_score = final_match_score + stage_two(
                            main_feed_item['quotes'], other_feed_item['quotes'])
                    except:
                        pass

                    try:
                        final_match_score = final_match_score + stage_three(
                            main_feed_item['sentences'], other_feed_item['sentences'])
                    except:
                        pass

                    try:
                        final_match_score = final_match_score + stage_four(
                            main_feed_item['tokenized_body'], other_feed_item['tokenized_body'])
                    except:
                        pass
                    if final_match_score > 65:
                        print ("\t" + str(final_match_score) + " Score for: " + other_feed_item['title'] + " " +
                               "    " + "(" + rss_feed.source + ")")

    return (match_table)


def test_redis():
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    return r