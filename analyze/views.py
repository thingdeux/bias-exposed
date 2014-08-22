from django.shortcuts import render
from analyze.models import PotentialStory, PotentialArticle
from analyze.models import WordDetail


def Index(request):
    stories = PotentialStory.objects.all()
    articles = PotentialArticle.objects.all().select_related()

    return render(request, 'analyze/index.html', {'stories': stories,
                                                  'articles': articles})


def Story(request, story):
    story = PotentialStory.objects.get(id=story)
    articles = PotentialArticle.objects.filter(
        potentialstory=story).select_related()
    words = WordDetail.objects.filter(potentialarticle=story)

    return render(request, 'analyze/story.html', {'story': story,
                                                  'articles': articles,
                                                  'words': words})
