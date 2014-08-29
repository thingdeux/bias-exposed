from django.shortcuts import render
from analyze.models import PotentialStory, PotentialArticle
from analyze.models import WordDetail
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings


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
def Worddelete(request):
    if request.POST:
        try:
            word_id = request.POST['worddetail']
            to_delete = WordDetail.objects.get(id=word_id)
            to_delete.delete()
            return HttpResponse(status=200)
        except Exception as err:
            print err
            return HttpResponse(status=500)


def Testfeedrss(request):
    from os import path
    feed = open(path.join(settings.BASE_DIR + "/analyze/test_data/test.rss"))
    return StreamingHttpResponse(streaming_content=feed,
                                 content_type='application/atom+xml')


def Testfeedstory(request, story):
    if story in [u'1', u'2', u'3']:
        body = "<!DOCTYPE HTML><html><head><title>Valid Story #" + str(story) + """
        </title><h1>The Best News Article</h1><p class="story">
        This is a "news" 'story' about the latest trend in racing!
        It\'s called "rev-running"! <br>Its existence is normally a mystery
        But this intrepid reporter has gained an exclusive behind the
        curtain walkthrough of what it\'s all about </p><p>None of this
        should be picked up, Umbrella, Sheep, Barely made</p></body></html>"""

        return HttpResponse(body, content_type='text/html')
