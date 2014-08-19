from django.shortcuts import render
from analyze.models import FeedSource, PotentialStory, PotentialArticle


def Index(request):
    feedSources = PotentialArticle.objects.all()
    return render(request, 'analyze/index.html', {'sources': feedSources})
