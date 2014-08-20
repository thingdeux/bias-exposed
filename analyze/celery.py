from __future__ import absolute_import

import os

from celery import Celery, chord
from django.conf import settings

# set the default Django settings module for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bias_exposed.settings')
from analyze.models import analyze_feed, FeedSource, compare_feed_to_others
from analyze.models import PotentialStory, PotentialArticle

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


@app.task
def check_all_feeds(allfeeds):
    potential_matches = {}
    for feed in allfeeds:
        try:
            compare_feed_to_others(feed, allfeeds, potential_matches)
        except Exception as err:
            print ("Unable to process feed: " + feed.source + "  " + str(err))

    # Delete any old feeds
    PotentialStory.objects.all().delete()
    # Iterate over the keys in the dictionary which will be
    # Hashes of source-id at index 0 and potential matches at 1
    # Potential Match Index:
    for key, matches in potential_matches.iteritems():
        if len(matches) > 1:
            story = PotentialStory(title=matches[0]['title'], first_key=key)
            story.save()
            bulk_insert_list = []

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
                    if not exists:
                        bulk_insert_list.append(new_record)

                except Exception as err:
                    print "Can't create DB record: " + str(err)
            PotentialArticle.objects.bulk_create(bulk_insert_list)

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
