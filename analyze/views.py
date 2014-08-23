from django.shortcuts import render
from analyze.models import PotentialStory, PotentialArticle
from analyze.models import WordDetail
from django.http import HttpResponse


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


def Reassign(request):
    if request.POST:
        article_id = request.POST['article']
        story = request.POST['to']
        to_reassign = PotentialArticle.objects.get(id=article_id)
        new_story = PotentialStory.objects.get(id=story)
        to_reassign.potentialstory = new_story
        to_reassign.save()
        return HttpResponse(status=200)


def Delete(request):
    if request.POST:
        try:
            article_id = request.POST['article']
            to_delete = PotentialArticle.objects.get(id=article_id)
            to_delete.delete()
            print ("Deleted")
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)
