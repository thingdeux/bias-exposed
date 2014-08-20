from django.shortcuts import render
from analyze.models import FeedSource, PotentialStory, PotentialArticle
from operator import itemgetter


def Index(request):
    stories = PotentialStory.objects.all()

    return render(request, 'analyze/index.html', {'stories': stories})
