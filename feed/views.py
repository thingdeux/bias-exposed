from django.shortcuts import render
from feed.models import Story, Feed, Word


def Index(request):
    stories = Story.objects.all()
    return render(request, 'feed/index.html', {'stories': stories})
