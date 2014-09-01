from django.shortcuts import render
from stories.models import Story, Article, Word, Detail
import json


def Index(request):
    stories = Story.objects.all()
    return render(request, 'stories/index.html', {'stories': stories})


def Storybyslug(request, **kwargs):
    slug_query = kwargs['slug']
    story = Story.objects.get(article_slug=slug_query)
    articles = Article.objects.filter(story=story).select_related()
    word_details = Detail.objects.filter(article__story=story).order_by('-usage').select_related()
    wordDict = {}

    shared_words = story.shared_words.split('|')

    for article in articles:
        wordDict[article.id] = [['Word', 'Usage']]
        for detail in word_details.filter(article=article)[:8]:
            wordDict[article.id].append([detail.word.word,
                                             detail.usage])

    return render(request, 'stories/story.html', {'story': story,
                                                  'articles': articles,
                                                  'wordDict': wordDict,
                                                  'shared_words': shared_words})

def Storyviewbyyear(request, **kwargs):
    print kwargs
    return render(request, 'stories/index.html')
