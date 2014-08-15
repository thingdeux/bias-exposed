from django.shortcuts import render
from analyze.models import FeedSource


def Index(request):
    feedSources = FeedSource.objects.all()
    return render(request, 'analyze/index.html', {'sources': feedSources})
