
from rssfeed import RSSFeed, get_stop_words


def compare_tokens(word_tokens_A, word_tokens_B):
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

# AP
rss_list.append(RSSFeed('http://hosted.ap.org/lineups/POLITICSHEADS.rss?SITE=AP&SECTION=HOME'))
# HuffingtonPost
rss_list.append(RSSFeed('http://www.huffingtonpost.com/feeds/verticals/politics/news.xml'))
# FoxNews
rss_list.append(RSSFeed('http://feeds.foxnews.com/foxnews/politics'))
# CNN
rss_list.append(RSSFeed('http://rss.cnn.com/rss/cnn_allpolitics.rss'))
# Reuters
rss_list.append(RSSFeed('http://feeds.reuters.com/Reuters/PoliticsNews?format=xml'))
# NPR
rss_list.append(RSSFeed('http://www.npr.org/rss/rss.php?id=1014'))
# NYT
rss_list.append(RSSFeed('http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml'))
# NBC
rss_list.append(RSSFeed('http://feeds.nbcnews.com/feeds/topstories'))
# Washington Post
rss_list.append(RSSFeed('http://feeds.washingtonpost.com/rss/rss_election-2012'))
# The Guardian
rss_list.append(RSSFeed('http://feeds.theguardian.com/theguardian/politics/rss'))
# ABC
rss_list.append(RSSFeed('http://feeds.abcnews.com/abcnews/politicsheadlines'))
# BBC
rss_list.append(RSSFeed('http://feeds.bbci.co.uk/news/politics/rss.xml'))
# WSJ
rss_list.append(RSSFeed('http://online.wsj.com/xml/rss/3_7085.xml'))