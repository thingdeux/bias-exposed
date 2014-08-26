from django.test import TestCase
from analyze.models import PotentialStory, PotentialWord, WordDetail, FeedSource, ParseRule
from analyze.models import analyze_all_feeds, analyze_feed
from analyze.models import create_initial_rss_feeds, create_initial_parse_rules
from analyze.models import get_parse_rule, compare_feed_to_others


# class RSSFeedTests(TestCase):

class ModelCreationTests(TestCase):
    def setUp(self):
        emptyDBCheck = FeedSource.objects.all()
        self.assertEqual(len(emptyDBCheck), 0)
        # Create new feed sources
        create_initial_rss_feeds()

    def test_creation_of_new_feed_sources(self):
        """
        Test the creation of new feed sources. Verify the DB is empty
        Then create sources and verify each one is populated.
        """
        # Make sure feed sources don't exist
        new_feed_sources = FeedSource.objects.all()
        self.assertGreaterEqual(len(new_feed_sources), 13)
    def test_creation_of_new_parse_rules(self):
        """
        Test creation of new parse rules.
        """
        # create_initial_rss_eeds()
        # Make sure parse rules don't exist
        emptyDBCheck = ParseRule.objects.all()
        self.assertEqual(len(emptyDBCheck), 0)
        # Create new parse rules
        create_initial_parse_rules()
        new_parse_rules = ParseRule.objects.all()
        self.assertGreaterEqual(len(new_parse_rules), 13)
