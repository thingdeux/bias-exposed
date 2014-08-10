
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
rss_list.append(RSSFeed('http://feeds.reuters.com/Reuters/PoliticsNews?format=xml'))
rss_list.append(RSSFeed('http://hosted.ap.org/lineups/POLITICSHEADS.rss?SITE=AP&SECTION=HOME'))
rss_list.append(RSSFeed('http://feeds.foxnews.com/foxnews/politics'))
rss_list.append(RSSFeed('http://rss.cnn.com/rss/cnn_allpolitics.rss'))
rss_list.append(RSSFeed('http://www.npr.org/rss/rss.php?id=1014'))
rss_list.append(RSSFeed('http://www.huffingtonpost.com/feeds/verticals/politics/news.xml'))
