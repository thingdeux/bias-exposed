# -*- coding: utf-8 -*-
from nltk import FreqDist
from nltk.tokenize.punkt import PunktWordTokenizer
import feedparser
from time import localtime
from bs4 import BeautifulSoup
from requests import get

# Some feeds have more than 40 entries (I'm looking at you CNN)
# Don't need that many.
FEED_LIMIT = 15


class RSSFeed:
    def __init__(self, feed_url, source_name):
        try:
            self.feed_url = feed_url
            # Parse the RSS Feed
            feed = feedparser.parse(self.feed_url)
            raw_feed_items = [a_feed for a_feed in feed['items']]
            self.feed_title = str(feed['channel']['title'])
            self.source = source_name
            self.feed_items = self.build_feed_list(raw_feed_items)
        except Exception as err:
            print err
            return None

    # Iterate over feedparser item feed and return list of feeds
    # With Urls, titles, ID's, datess, and body text.
    def build_feed_list(self, feed_items):
        def check_item_exists(check_string):
            try:
                # Check at least 3 feeds for the existence
                # Of the item parameter
                for a_feed in feed_items[:3]:
                    if len(a_feed[check_string]) > 0:
                        pass
                    else:
                        raise NameError
                        return False
                return True
            except Exception as err:
                print ("Unable to find " + str(err) +
                       " on " + str(self.source))
                return False

        try:
            feed_has_title = check_item_exists('title')
            feed_has_link = check_item_exists('link')
            feed_has_date = check_item_exists('published_parsed')
            parsed_items = []

            # There's no need to process the RSS items if they don't
            # have titles and feed links
            if feed_has_title is True and feed_has_link is True:
                for count, feed_item in enumerate(feed_items[:FEED_LIMIT]):                    
                    raw_html = self.get_http_content(feed_item['link'])
                    story = {
                        'id': count,
                        'title': feed_item['title'],
                        'tokenized_title': self.tokenize_string(
                            feed_item['title']),
                        'link': feed_item['link'],
                        'raw_html': raw_html,
                        'quotes': self.build_quote_list(raw_html)
                        }
                    # If there's a published date add it.
                    if feed_has_date:
                        story['date'] = feed_item['published_parsed']
                    else:
                        story['date'] = localtime()

                    parsed_items.append(story)

                return (parsed_items)
            else:
                return None
        except Exception as err:
            print "Unable to build feed items " + str(err)
            return None

    # Turn raw strings to word tokens usable by nltk
    def tokenize_string(self, passed_string):        
        if len(passed_string) > 0:
            return (PunktWordTokenizer().tokenize(passed_string))

    # Acquire a frequency distribution of tokens
    def get_frequency_dist(self, tokenized_string):
        return FreqDist(tokenized_string)

    # Return a list of words that are of a specified list and
    # used more than a certain amount of times.
    # Default is 3 characters long and used thrice.
    def find_common_usage(self, length_at_least=3, times_word_used=3):
        return sorted(word.lower() for word in set(self.tokenized_string)
                      if len(word) >= length_at_least and
                      self.frequency_distribution[word] >= times_word_used and
                      word.lower() not in get_stop_words())  

    def build_quote_list(self, string):        
        quotePositions = []
        quotes = []
        # Iterate over the string and store the position of each parenthesis
        for count, letter in enumerate(string):
            if letter == '"' or letter == u'\u201d' or letter == u'\u201c':
                quotePositions.append(count)

        # Iterate over the stored parethesis positions two at a time
        # add each quote block to a list and return it.
        for count, position in enumerate(sorted(quotePositions)):
            if count % 2 == 0 or count == 0:
                try:
                    quotes.append(string[quotePositions[count] + 1:
                                         quotePositions[count + 1]])
                except Exception as err:
                    print err
                    pass
        if len(quotes) >= 1:
            return quotes
        else:
            return None

    # Refactor ......... SLOW!!
    def get_http_content(self, url):
        # Use requests library to perform a get request against url
        http_request = get(url)
        # process the raw html into a beautiful soup object
        raw_html = BeautifulSoup(http_request.text)
        # Perform css filter query
        selected_html = raw_html.select(get_article_dom_id(self.source))
        to_return = ""
        # Remove all tags and transform the html into a string
        for element in selected_html:
            try:
                to_return = to_return + element.text
            except:
                pass
        return (to_return)


# Common english words that should be excluded from the analysis
def get_stop_words():
    stopWords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours',
                    'ourselves', 'you', 'your', 'yours', 'yourself',
                     'yourselves', 'he', 'him', 'his', 'himself', 'she',
                     'her', 'hers', 'herself', 'it', 'its', 'itself', 'they',
                     'them', 'their', 'theirs', 'themselves', 'what', 'which',
                     'who', 'whom', 'this', 'that', 'these', 'those', 'am',
                     'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
                     'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a',
                     'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
                     'until', 'while', 'of', 'at', 'by', 'for', 'with',
                     'about', 'against', 'between', 'into', 'through', 'on',
                     'before', 'after', 'above', 'below', 'to', 'from', 'up',
                     'down', 'in', 'out', 'off', 'over', 'under', 'again',
                     'further', 'then', 'once', 'here', 'there', 'when',
                     'where', 'why', 'how', 'all', 'any', 'both', 'each',
                     'few', 'more', 'most', 'other', 'some', 'such', 'no',
                     'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
                     'very', 's', 't', 'can', 'will', 'just', 'don', 'should',
                     'now', 'said', 'the', 'said', 'the', 'could', 'during',
                     ','])

    return stopWords


def get_article_dom_id(string):
    # Hacky, don't like it
    from models import get_parse_rule
    return (get_parse_rule(string))
