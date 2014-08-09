from nltk import FreqDist
from nltk.tokenize.punkt import PunktWordTokenizer
import feedparser


class RSSFeed:
    def __init__(self, feed_url):
        try:
            self.feed_url = feed_url
            # Parse the RSS Feed
            feed = feedparser.parse(self.feed_url)
            raw_feed_items = [a_feed for a_feed in feed['items']]
            self.source = str(feed['channel']['title'])
            self.feed_items = self.build_feed_list(raw_feed_items)
        except Exception as err:
            print err
            return None

    def build_feed_list(self, feed_items):
        new_items = [{'id': num,
                      'title': a_feed['title'],
                      'tokenized_title': self.tokenize_string(a_feed['title']),
                      'link': a_feed['link'],
                      'date_published': a_feed['published_parsed']}
                     for num, a_feed in enumerate(feed_items)]
        return (new_items)

    def analyze_text(self, passed_string):
        try:
            self.passed_string = passed_string
            self.tokenized_string = self.tokenize_string(self.passed_string)
            self.frequency_distribution = self.get_frequency_dist(
                self.tokenized_string)
        except Exception as err:
            print err
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
    # Default is 3 characters long and used at least thrice.
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

def find_similarity(word_tokens_A, word_tokens_B):
    def strip_stop_words(token_list):
        return (word.lower() for word in token_list
                if word.lower() not in get_stop_words())

    # Casting to set for speed boost, order does not matter.
    comparison_a = set(strip_stop_words(word_tokens_A))
    comparison_b = set(strip_stop_words(word_tokens_B))
    rank = 0

    for word in comparison_a:
        if word in comparison_b:
            rank = rank + 1

    return rank


rss_list = []
#rss_list.append(RSSFeed('http://feeds.reuters.com/Reuters/PoliticsNews?format=xml'))
rss_list.append(RSSFeed('http://feeds.foxnews.com/foxnews/politics'))
rss_list.append(RSSFeed('http://rss.cnn.com/rss/cnn_allpolitics.rss'))
rss_list.append(RSSFeed('http://www.npr.org/rss/rss.php?id=1014'))
rss_list.append(RSSFeed('http://www.huffingtonpost.com/feeds/verticals/politics/news.xml'))

check_similarity_to = PunktWordTokenizer().tokenize("Obama signs bill to fix delays in veterans healthcare")  # noqa
print "Checking: Obama signs bill to fix delays in veterans healthcare"


for rss_feed in rss_list:
    print rss_feed.source
    for item in rss_feed.feed_items:
        rank = find_similarity(PunktWordTokenizer().tokenize(item['title']), check_similarity_to)
        if rank > 2:
            print (str(rank) + "  --->   " + item['title'] + item['link'])
