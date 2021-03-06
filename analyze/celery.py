from __future__ import absolute_import

import os

from celery import Celery, chord
from django.conf import settings

# set the default Django settings module for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bias_exposed.settings')
from analyze.models import analyze_feed, FeedSource, compare_feed_to_others
from analyze.models import PotentialStory, PotentialArticle, PotentialWord
from analyze.models import WordDetail
from stories.models import Story, Word, Article, Detail
from django.utils.text import slugify

app = Celery('analyze')

# Pull celery config info from Django Settings.
app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


"""
Celery Tasks
Each task will spin off it's own celery process
"""


# Task for crawling/processing 1 RSS Feed
@app.task(time_limit=90)
def queueFeed(feed_name):
    def check_feed_integrity(feed):
        try:
            # Check to make sure there are articles in the feed
            # Before putting it through for analysis
            if len(feed.feed_items) > 2:
                return True
            else:
                # Update DB Parse Rule for invalid
                return False
        except Exception as err:
            print ("Not a valid feed: " + str(err))
            return False

    processed_feed = analyze_feed(feed_name)
    if check_feed_integrity(processed_feed):
        return processed_feed
    else:
        return None


# Task for checking all feeds and creating potential matching pairs
@app.task
def check_all_feeds(allfeeds):
    potential_matches = {}
    for feed in allfeeds:
        try:
            compare_feed_to_others(feed, allfeeds, potential_matches)
        except Exception as err:
            print ("Unable to process feed: " + feed.source + "  " + str(err))

    # Delete any old feeds
    PotentialArticle.objects.all().delete()
    PotentialStory.objects.all().delete()
    # Iterate over the keys in the dictionary which will be
    # Hashes of source-id at index 0 and potential matches at 1
    # Potential Match Index:
    for key, matches in potential_matches.iteritems():
        if len(matches) > 1:
            story = PotentialStory(title=matches[0]['title'], first_key=key)
            story.save()
            bulk_insert_articles = []
            bulk_insert_word_details = []

            for match in matches:
                try:
                    # final_score|reasons|key|feed_obj|isProcessed|source
                    new_record, exists = PotentialArticle.objects.get_or_create(
                        potentialstory=story, source=match['source'],
                        title=match['feed_item_obj']['title'],
                        url=match['feed_item_obj']['link'],
                        final_match_score=match['final_score'],
                        match_title=match['reasons']['title'],
                        match_body=match['reasons']['body'],
                        match_quotes=match['reasons']['quotes'],
                        match_sentences=match['reasons']['sentences'],
                        match_key=match['key'])

                    try:
                        for word, count in match['feed_item_obj']['word_usage'].iteritems():
                            word_to_use, word_exists = PotentialWord.objects.get_or_create(word=word)
                            bulk_insert_word_details.append(
                                WordDetail(potentialword=word_to_use,
                                           potentialarticle=new_record,
                                           usage=count
                                           ))
                    except Exception as err:
                        print (err)

                    if not exists:
                        bulk_insert_articles.append(new_record)

                except Exception as err:
                    print "Can't create DB record: " + str(err)
            PotentialArticle.objects.bulk_create(bulk_insert_articles)
            WordDetail.objects.bulk_create(bulk_insert_word_details)

            # Combine potential matches into one potential story.
            for main_story in PotentialStory.objects.all():
                # Find all of the stories that have a reference to
                # This first key.
                stories = PotentialStory.objects.filter(
                    potentialarticle__match_key=main_story.first_key).exclude(
                        id=main_story.id)
                # Pull out the articles from that object and relate them
                # All to the original if they aren't already.
                # Remove the others
                for story in stories:
                    articles = PotentialArticle.objects.filter(
                        potentialstory=story)

                    for article in articles:
                        if len(articles) > 0:
                            if PotentialArticle.objects.filter(
                                    potentialstory=main_story,
                                    match_key=article.match_key).exists():
                                article.delete()
                            else:
                                article.potentialstory = main_story
                                article.save()

    # Clean up any stories that don't have matches
    PotentialStory.objects.filter(potentialarticle__match_key=None).delete()
    print ("Matches complete")
    return ([allfeeds, potential_matches])


@app.task
def compare_tests():
    callback = check_all_feeds.s()
    # Spin up a process for each of the feed gatherers, when they're
    # all complete call check_all_feeds
    head = [queueFeed.s(feed.source) for feed in FeedSource.objects.filter(
            parserule__caused_error=False)]
    result = chord(head)(callback)

    return result


@app.task
def publish_story(story_id):
    def process_shared_words(querySet, halfOfArticles):
        # Building a dictionary with words as indexes so that I can see how
        # many articles Re-Use the same word, if at least half of them re-use
        # a word that word will be Added to the "agreed upon" words for
        # the story and filtered out of the final Analysis.
        shared_dict = {}
        for detail in potentialWords:
            try:
                shared_dict[detail.potentialword.word].append(detail)
            except:
                shared_dict[detail.potentialword.word] = [detail]

        shared_words = ""
        for key, value in shared_dict.iteritems():
            try:
                if len(value) > halfOfArticles:
                    print ("Deleting: " + key)
                    for detail in value:
                        detail.delete()
                    shared_words = shared_words + key + "|"
            except Exception as err:
                print "Couldn't create dict: " + str(err)

        return shared_words

    potentialStory = PotentialStory.objects.get(id=story_id)
    if potentialStory:
        print (u"Publishing " + potentialStory.title)
        try:
            title_slug = slugify(potentialStory.title)
            story = Story(title=potentialStory.title, article_slug=title_slug,
                          tag=potentialStory.tag)
            story.save()
            potentialArticles = PotentialArticle.objects.filter(
                potentialstory=potentialStory).select_related()
            potentialWords = WordDetail.objects.filter(
                potentialarticle__potentialstory=potentialStory).select_related()

            # If at least half of the articles re-use the same words remove
            # them from the final analysis
            half_of_total_articles = len(potentialArticles) / 2
            sharedWords = process_shared_words(potentialWords,
                                               half_of_total_articles)
            story.shared_words = sharedWords
            story.save()

            bulk_insert_details = []
            for article in potentialArticles:
                # Process article
                try:
                    newArticle = Article(story=story, source=article.source,
                                         title=article.title, url=article.url)
                    newArticle.save()
                    # Process words and word details
                    try:
                        for word_detail in WordDetail.objects.filter(
                                potentialarticle=article):
                            word_to_use, exists = Word.objects.get_or_create(
                                word=word_detail.potentialword.word)
                            bulk_insert_details.append(
                                Detail(word=word_to_use,
                                       article=newArticle,
                                       usage=word_detail.usage))
                    except Exception as err:
                        print err

                except Exception as err:
                    print err

            Detail.objects.bulk_create(bulk_insert_details)

        except Exception as err:
            print ("Unable to publish story: " + str(story_id))
            print err
