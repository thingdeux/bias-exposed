from django.test import TestCase, LiveServerTestCase
from analyze.models import PotentialStory, PotentialWord, WordDetail
from analyze.models import analyze_all_feeds, analyze_feed, ParseRule
from analyze.models import create_initial_rss_feeds, create_initial_parse_rules
from analyze.models import get_parse_rule, compare_feed_to_others, FeedSource
from analyze.rssfeed import RSSFeed


class RSSFeedTests(LiveServerTestCase):
    def setUp(self):
        """
        I Created an RSS feed view specifically for testing at
        /analyze/Testfeedrss. Create test feed source and parse
        rules.
        """
        feedSource = FeedSource(source="TEST",
                                rss_feed_url=self.live_server_url + '/analyze/testfeed')  # noqa
        feedSource.save()
        rule = ParseRule(source=feedSource, dom_selector=".story")
        rule.save()

    def test_404_http_response_from_feed(self):
        """
        Perform a GET request against a passed feed URL and get a 404.
        Feed object still created but without necessary attributes.
        """
        # Not a valid url
        testfeed = RSSFeed(self.live_server_url + "/analyze/1234", "TEST")
        # Feed URL and source should be created but nothing else should pass
        self.assertEqual(testfeed.feed_url, self.live_server_url + '/analyze/1234')  # noqa
        self.assertEqual(testfeed.source, "TEST")

        # Make sure none of the below values exist and raise an attribute error
        with self.assertRaises(AttributeError):
            testfeed.feed
        with self.assertRaises(AttributeError):
            testfeed.feed_items
        with self.assertRaises(AttributeError):
            testfeed.feed_title

    def test_response_with_no_feed_content(self):
        """
        Perform a GET request against a passed feed URL and receive
        A response but no valid atom/xml RSS Feed data to parse.
        """
        # Valid URL, no RSS Feed
        testfeed = RSSFeed(self.live_server_url + "/analyze/testfeed/1", "TEST")
        self.assertEqual(testfeed.feed_url, self.live_server_url + "/analyze/testfeed/1")
        self.assertEqual(testfeed.source, "TEST")
        # Make sure none of the below values exist and raise an attribute error
        with self.assertRaises(AttributeError):
            testfeed.feed
        with self.assertRaises(AttributeError):
            testfeed.feed_items

    def test_response_with_feed_content(self):
        """
        Use a valid url to access a test RSS Feed with basic data.
        """
        testfeed = RSSFeed(self.live_server_url + "/analyze/testfeed", "TEST")
        self.assertEquals(len(testfeed.feed_items), 6)


class ModelCreationTests(TestCase):
    def setUp(self):
        """
        Initial feed rules/sources setup.
        Verify the DB is empty Then create sources
        and verify each one is populated below.
        """
        emptyDBCheck = FeedSource.objects.all()
        self.assertEqual(len(emptyDBCheck), 0)
        # Create new feed sources
        create_initial_rss_feeds()
        # Make sure parse rules don't exist
        emptyDBCheck = ParseRule.objects.all()
        self.assertEqual(len(emptyDBCheck), 0)
        # Create new parse rules
        create_initial_parse_rules()

    def test_creation_of_new_feed_sources(self):
        """
        Test the creation of new feed sources.
        """
        # Make sure feed sources don't exist
        new_feed_sources = FeedSource.objects.all()
        self.assertGreaterEqual(len(new_feed_sources), 13)

    def test_creation_of_new_parse_rules(self):
        """
        Test creation of new parse rules.
        """
        new_parse_rules = ParseRule.objects.all()
        self.assertGreaterEqual(len(new_parse_rules), 13)

    def test_get_parse_rule(self):
        """
        Pass in a number of successful parameters and check
        that they return the proper parse rule.
        """
        ap = get_parse_rule("AP")
        self.assertEqual(ap, ".entry-content")
        nyt = get_parse_rule("NYT")
        self.assertEqual(nyt, "#story > p")
        bbc = get_parse_rule("BBC")
        self.assertEqual(bbc, ".story-body > p")

    def test_incorrect_get_parse_rule(self):
        """
        Pass incorrect parameter to parse rule. Should return None
        """
        incorrect = get_parse_rule("Teddy Bear")
        self.assertEqual(incorrect, None)

    def test_empty_string_parse_rule(self):
        """
        Pass empty string paramter to parse request.
        Should return None.
        """
        empty = get_parse_rule("")
        self.assertEqual(empty, None)
