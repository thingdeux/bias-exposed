from nltk import FreqDist
from nltk.tokenize.punkt import PunktWordTokenizer
import feedparser
from time import localtime
from bs4 import BeautifulSoup
from requests import get


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
                for count, feed_item in enumerate(feed_items):
                    story = {
                        'id': count,
                        'title': feed_item['title'],
                        'tokenized_title': self.tokenize_string(feed_item['title']),
                        'link': feed_item['link']
                        #'quotes': self.build_quote_list()
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

    # Return a list of words that are used more than a certain amount of times.
    # And are used at least a certain amount of times.
    # Default is 3 characters long and used ahrice.
    def find_common_usage(self, length_at_least=3, times_word_used=3):
        return sorted(word.lower() for word in set(self.tokenized_string)
                      if len(word) >= length_at_least and
                      self.frequency_distribution[word] >= times_word_used and
                      word.lower() not in get_stop_words())

    def simple_test_print(self, name, length=3, times_used=3):
        print (str(name) + ": ")
        for word in self.find_common_usage(length, times_used):
            print ("   " + word)
        print ("\n\n")

    def build_quote_list(string):
        quotePositions = []
        quotes = []
        # Iterate over the string and store the position of each parenthesis
        for count, letter in enumerate(string):
            if letter is '"':
                quotePositions.append(count)

        # Iterate over the stored parethesis positions two at a time
        # add each block to and return quotes list
        for count, position in enumerate(sorted(quotePositions)):
            if count % 2 == 0:
                try:
                    quotes.append(string[quotePositions[count] + 1:
                                         quotePositions[count + 1]])
                except:
                    pass
        return quotes


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


def get_article_dom_id(feed):
    if feed == "AP":
        return ("CLASS", ".entry-content")
    elif feed == "HuffingtonPost":
        return ("ID", "#mainentrycontent")
    elif feed == "FoxNews":
        # Further Clarification may be needed
        return ("TAG", "<article>")
    elif feed == "CNN":
        # Story is attached to Multiple Classes
        return ("CLASS", "cnn_strylftcntnt > p")
    elif feed == "Reuters":
        return ("ID", "#articleText")
    elif feed == "NPR":
        return ("ID", "#storytext")
    elif feed == "NYT":
        return ("ID", "#story > p")
    elif feed == "NBC":
        return ("CLASS", ".stack-l-content")
    elif feed == "WashingtonPost":
        return ("ID", "#article-body")
    elif feed == "TheGuardian":
        return ("ID", "#article-body-blocks")
    elif feed == "ABC":
        return ("ID", "#innerbody > p")
    elif feed == "BBC":
        return ("CLASS", ".story-body > p")
    elif feed == "WSJ":
        return ("ID", "#articleBody")   

if __name__ == "__main__":
    test = RSSFeed('http://www.huffingtonpost.com/feeds/verticals/politics/news.xml', "HuffingtonPost")
    http_request = get(test.feed_items[0]['link'])
    #print http_request.text
    #BeautifulSoup(get(feed_item['link']).text)
    