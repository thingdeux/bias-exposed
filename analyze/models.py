from django.db import models
# from feed.models import Story, Feed, Word
from rssfeed import RSSFeed
from django.conf import settings
from django import forms


class PotentialStory(models.Model):
    # Title of the major news story
    title = models.TextField(max_length=1024, default="")
    first_key = models.CharField(max_length=50)
    tag = models.TextField(max_length=512, default="")

    def __unicode__(self):
        return self.title


class PotentialStoryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=1024)
    tag = forms.CharField(label="Tagline", max_length=512)

class PotentialWord(models.Model):
    word = models.CharField(max_length=512, unique=True)

    def __unicode__(self):
        return self.word


class PotentialArticle(models.Model):
    potentialstory = models.ForeignKey(PotentialStory)
    source = models.CharField("Article Source", max_length=50)
    # Feed Title
    title = models.CharField("Title", max_length=512)
    # RSS Feed URL
    url = models.URLField("URL", max_length=2000)
    final_match_score = models.PositiveIntegerField("Total Match Score",
                                                    default=0)
    match_title = models.PositiveIntegerField("Title Match", default=0)
    match_body = models.PositiveIntegerField("Body Match", default=0)
    match_quotes = models.PositiveIntegerField("Quote Match", default=0)
    match_sentences = models.PositiveIntegerField("Sentence Match", default=0)
    match_key = models.CharField(max_length=50)
    words = models.ManyToManyField(PotentialWord, through='WordDetail')

    def __unicode__(self):
        return (self.source + ": " + str(self.final_match_score))


class WordDetail(models.Model):
    potentialword = models.ForeignKey(PotentialWord)
    potentialarticle = models.ForeignKey(PotentialArticle)
    usage = models.PositiveIntegerField(default=1)


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
        ["http://hosted.ap.org/lineups/POLITICSHEADS.rss?SITE=AP&SECTION=HOME", "AP"],  # noqa
        ["http://www.huffingtonpost.com/feeds/verticals/politics/news.xml", "HuffingtonPost"],  # noqa
        ["http://feeds.foxnews.com/foxnews/politics", "FoxNews"],
        ["http://rss.cnn.com/rss/cnn_allpolitics.rss", "CNN"],
        ["http://feeds.reuters.com/Reuters/PoliticsNews?format=xml", "Reuters"],  # noqa
        ["http://www.npr.org/rss/rss.php?id=1014", "NPR"],
        ["http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml", "NYT"],
        ["http://feeds.nbcnews.com/feeds/topstories", "NBC"],
        ["http://feeds.washingtonpost.com/rss/rss_election-2012", "WashingtonPost"],  # noqa
        ["http://feeds.theguardian.com/theguardian/politics/rss", "TheGuardian"],  # noqa
        ["http://feeds.abcnews.com/abcnews/politicsheadlines", "ABC"],
        ["http://feeds.bbci.co.uk/news/politics/rss.xml", "BBC"],
        ["http://america.aljazeera.com/content/ajam/articles.rss", "Aljazeera"]
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
        [FeedSource.objects.get(source="HuffingtonPost"), "#mainentrycontent > p"],  # noqa
        [FeedSource.objects.get(source="FoxNews"), "article"],
        [FeedSource.objects.get(source="CNN"), ".cnn_storypgraphtxt"],
        [FeedSource.objects.get(source="Reuters"), "#articleText"],
        [FeedSource.objects.get(source="NPR"), "#storytext"],
        [FeedSource.objects.get(source="NYT"), "#story > p"],
        [FeedSource.objects.get(source="NBC"), ".stack-l-content"],
        [FeedSource.objects.get(source="WashingtonPost"), "#article-body"],
        [FeedSource.objects.get(source="TheGuardian"), "#article-body-blocks"],
        [FeedSource.objects.get(source="ABC"), "#innerbody > div > p"],
        [FeedSource.objects.get(source="BBC"), ".story-body > p"],
        [FeedSource.objects.get(source="Aljazeera"), ".text section > p"]
    ]

    bulk_list = []
    for rule in PARSE_RULES:
        bulk_list.append(ParseRule(source=rule[0], dom_selector=rule[1]))

    ParseRule.objects.bulk_create(bulk_list)


def get_parse_rule(feed_name):
    try:
        # Should only ever be one parse rule per feed.
        rule = ParseRule.objects.get(source__source=feed_name)
        return (rule.dom_selector)
    except:
        return None


def compare_feed_to_others(main_feed, all_feeds, dictionary):
    def stage_one(main_title, other_title):
        match_score = 0
        try:
            for word in main_title:
                if word in other_title:
                    match_score += 15
        except:
            pass
        return match_score

    def stage_two(main_quotes, other_quotes):
        """
        Stage one article comparison, check to see if there article
        shared quotes between the two articles
        """
        match_score = 0
        # Check to see if each quote in the current article is in another_feeds
        # Quote list
        try:
            for quote in main_quotes:
                if quote in other_quotes:
                    match_score += 30
        except:
            pass
        return match_score

    def stage_three(main_sentences, other_sentences):
        match_score = 0
        try:
            for main_sentence in main_sentences:
                # Make sure the sentence is at least 3 words long
                # Should catch false positives like 'Gen.' or 'Sen.'
                if len(main_sentence.split(' ')) > 3:
                    if main_sentence in other_sentences:
                        match_score += 15
        except:
            pass
        return match_score

    def stage_four(main_body_tokens, other_body_tokens):
        match_score = 0
        try:
            for token in main_body_tokens:
                if token in other_body_tokens:
                    match_score += .25
        except:
            pass
        return match_score

    def compare_to_other_feed_items():
        # Iterate over the main_feeds articles one at a time
        for main_feed_item in main_feed.feed_items:
            # Iterate over each RSSFeed Object in the all_feeds list
            for rss_feed in all_feeds:
                try:
                    # Make sure to skip the RSSFeed Obj that equals main_feed
                    if main_feed.source is not rss_feed.source:
                        for other_feed_item in rss_feed.feed_items:
                            match_score = {}
                            # Try to find related articles across feeds using
                            # The algorithm defined in 'the_plan.txt'
                            # Stage 1 matches based on title tokens
                            # Stage 2 matches on matching quotes
                            # Stage 3 matches on matching sentences
                            # Stage 4 matches on tokens from article content
                            # The final score is kept along with the reasons
                            # For the rating (passed along as a dictionary)
                            try:
                                match_score['title'] = stage_one(
                                    main_feed_item['tokenized_title'],
                                    other_feed_item['tokenized_title'])
                            except:
                                pass

                            try:
                                match_score['quotes'] = stage_two(
                                    main_feed_item['quotes'],
                                    other_feed_item['quotes'])
                            except:
                                pass

                            try:
                                match_score['sentences'] = stage_three(
                                    main_feed_item['sentences'],
                                    other_feed_item['sentences'])
                            except:
                                pass

                            try:
                                match_score['body'] = stage_four(
                                    main_feed_item['tokenized_body'],
                                    other_feed_item['tokenized_body'])
                            except:
                                pass

                            final_match_score = 0
                            for score in match_score.keys():
                                final_match_score += match_score[score]

                            # The key used for the matching dictionary is a
                            # String composed of 'Feed Source' followed by a
                            # - and the feed ID number
                            if final_match_score >= 40 and match_score['title'] > 0:
                                main_dict_key = str(
                                    main_feed.source) + "-" + str(
                                    main_feed_item['id'])
                                other_dict_key = str(
                                    rss_feed.source) + "-" + str(
                                    other_feed_item['id'])
                                match = {
                                    # Feed Object
                                    'feed_item_obj': other_feed_item,
                                    'source': rss_feed.source,
                                    'key': other_dict_key,
                                    # Int of the total score of a feed match
                                    'final_score': final_match_score,
                                    # Dictionary with the broken down score of
                                    # The reason each match was made.
                                    'reasons': match_score,
                                    # Used to determine if the feed has been
                                    # Processed when creating a model entry.
                                    'isProcessed': False,
                                    'title': main_feed_item['title']                                    
                                }

                                try:
                                    # Append entry to final match table
                                    dictionary[main_dict_key].append(match)
                                except:
                                    try:
                                        # Create entry for final match table
                                        dictionary[main_dict_key] = [match]
                                    except Exception as err:
                                        print ("Can't create match: " + err)

                except:
                    # print (err)
                    pass

    if main_feed is not None and all_feeds is not None:
        compare_to_other_feed_items()
