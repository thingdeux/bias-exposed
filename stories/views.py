from django.shortcuts import render
from stories.models import Story, Article, Word, WordDetail


def Index(request):
    stories = Story.objects.all()
    return render(request, 'stories/index.html', {'stories': stories})
