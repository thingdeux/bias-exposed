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
        self.testfeed = RSSFeed(self.live_server_url + "/analyze/testfeed",
                                "TEST")

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
        testfeed = RSSFeed(self.live_server_url + "/analyze/testfeed/1",
                                                  "TEST")
        self.assertEqual(testfeed.feed_url,
                         self.live_server_url + "/analyze/testfeed/1")
        self.assertEqual(testfeed.source, "TEST")
        # Make sure none of the below values exist and raise an attribute error
        with self.assertRaises(AttributeError):
            testfeed.feed
        with self.assertRaises(AttributeError):
            testfeed.feed_items

    def test_response_with_feed_content(self):
        """
        Use a valid url to test an RSS Feed with basic data.
        Make sure there's a feed_title assigned to the class,
        And make sure that each of the feed items has been
        retrieved
        """
        # Of the 6 feeds 2 of them should fail, make sure only 4 feed items
        # Are returned
        self.assertEqual(len(self.testfeed.feed_items), 4)
        self.assertEqual(self.testfeed.feed_title, u'test feed')

    def test_feed_items_properly_parsed(self):
        """
        Retrieve RSS Feed items from a valid url and ensure they've
        Been properly parsed.
        """
        # Test that titles have been changed to all lowercase characters
        self.assertEqual(self.testfeed.feed_items[0]['title'], u'story #1')
        self.assertEqual(self.testfeed.feed_items[1]['title'], u'story #2')
        # Test that links have been acquired for feed items
        self.assertEqual(self.testfeed.feed_items[2]['link'],
                         u'http://localhost:8081/analyze/testfeed/3')
        self.assertEqual(self.testfeed.feed_items[3]['link'],
                         u'http://localhost:8081/analyze/testfeed/4')
        # Test that stories 5 and 6 failed due to not having a link and title
        with self.assertRaises(IndexError):
            self.testfeed.feed_items[4]
        with self.assertRaises(IndexError):
            self.testfeed.feed_items[5]

    def test_feed_item_tokenized_title(self):
        """
        Make sure the RSSFeed Item titles are properly tokenized
        """
        self.assertEqual(self.testfeed.feed_items[0]['tokenized_title'],
                                                    [u'story', u'#1'])
        self.assertEqual(self.testfeed.feed_items[1]['tokenized_title'],
                                                    [u'story', u'#2'])
        self.assertEqual(self.testfeed.feed_items[2]['tokenized_title'],
                                                    [u'story', u'#3'])
        self.assertEqual(self.testfeed.feed_items[3]['tokenized_title'],
                                                    [u'story', u'#4'])

    def test_feed_item_quotes(self):
        """
        Make sure quotes have been parsed, should return a list item.
        With strings.
        """
        self.assertEqual(self.testfeed.feed_items[0]['quotes'],
                                                    ['news', 'rev-running'])
        self.assertEqual(self.testfeed.feed_items[1]['quotes'],
                                                    ['news', 'rev-running'])
        # No quotes are rendered for stream #4 - verify no quotes are caught
        self.assertEqual(self.testfeed.feed_items[3]['quotes'], None)

    def test_feed_raw_html(self):
        """
        Make sure the RAW HTML was pulled from the rss feed
        """
        # Story #4 should have no raw html
        self.assertEqual(self.testfeed.feed_items[3]['raw_html'], '')
        self.assertEqual(len(self.testfeed.feed_items[1]['raw_html']), 260)

    def test_feed_link_retrieved(self):
        """
        Make sure the feed links were retrieved
        """
        self.assertEqual(self.testfeed.feed_items[0]['link'],
                         'http://localhost:8081/analyze/testfeed/1')
        self.assertEqual(self.testfeed.feed_items[1]['link'],
                         'http://localhost:8081/analyze/testfeed/2')
        self.assertEqual(self.testfeed.feed_items[4]['link'],
                         'http://localhost:8081/analyze/testfeed/5')


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
