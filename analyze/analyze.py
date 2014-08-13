
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