from django.shortcuts import render
from analyze.models import PotentialStory, PotentialArticle
from analyze.models import WordDetail
from django.http import HttpResponse
from django.views.decorators.csrf import requires_csrf_token, ensure_csrf_cookie


@ensure_csrf_cookie
def Index(request):
    stories = PotentialStory.objects.all()
    articles = PotentialArticle.objects.all().select_related()

    return render(request, 'analyze/index.html', {'stories': stories,
                                                  'articles': articles})


@ensure_csrf_cookie
def Story(request, story):
    story = PotentialStory.objects.get(id=story)
    articles = PotentialArticle.objects.filter(
        potentialstory=story).select_related()
    words = WordDetail.objects.filter(
        potentialarticle__potentialstory=story).select_related().order_by('-usage')

    return render(request, 'analyze/story.html', {'story': story,
                                                  'articles': articles,
                                                  'words': words})


@requires_csrf_token
def Reassign(request):
    if request.POST:
        article_id = request.POST['article']
        story = request.POST['to']
        to_reassign = PotentialArticle.objects.get(id=article_id)
        new_story = PotentialStory.objects.get(id=story)
        to_reassign.potentialstory = new_story
        to_reassign.save()
        return HttpResponse(status=200)


@requires_csrf_token
def Delete(request):
    if request.POST:
        try:
            article_id = request.POST['article']
            to_delete = PotentialArticle.objects.get(id=article_id)
            to_delete.delete()
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)


@requires_csrf_token
def Delete_Word_Detail(request):
    if request.POST:
        try:
            word_id = request.POST['worddetail']
            to_delete = WordDetail.objects.get(id=word_id)
            to_delete.save()
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)
