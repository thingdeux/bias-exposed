from django.shortcuts import render
from stories.models import Story, Feed, Word


def Index(request):
    stories = Story.objects.all()
    return render(request, 'feed/index.html', {'stories': stories})
