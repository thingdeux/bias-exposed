from django.shortcuts import render
from analyze.models import FeedSource, PotentialStory, PotentialArticle
from operator import itemgetter


def Index(request):
    feedSources = PotentialArticle.objects.values('match_key').order_by('match_key')
    counts = {}

    for result in feedSources:
        for key, val in result.iteritems():
            try:
                counts[val] += 1
            except:
                counts[val] = 1

    sorted_count = sorted(counts.items(), key=itemgetter(1), reverse=True)

    return render(request, 'analyze/index.html', {'Potentials': sorted_count})
