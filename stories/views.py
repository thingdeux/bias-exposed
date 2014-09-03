from django.shortcuts import render
from stories.models import Story, Article, Detail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

MAX_ARTICLES_PER_PAGE = 10

def Index(request):
    stories = Story.objects.all()
    # Handler to manage paginator
    paginator = Paginator(stories, MAX_ARTICLES_PER_PAGE)
    page = request.GET.get('page')

    try:
        stories = paginator.page(page)
    except PageNotAnInteger:
        stories = paginator.page(1)
    except EmptyPage:
        stories = paginator.page(paginator.num_pages)

    return render(request, 'stories/index.html', {'stories': stories})


def Storybyslug(request, **kwargs):
    slug_query = kwargs['slug']
    story = Story.objects.get(article_slug=slug_query)
    articles = Article.objects.filter(story=story).select_related()
    word_details = Detail.objects.filter(article__story=story).order_by(
        '-usage').select_related()
    wordDict = {}

    shared_words = story.shared_words.split('|')

    for article in articles:
        wordDict[article.id] = [['Word', 'Usage']]
        for detail in word_details.filter(article=article)[:8]:
            wordDict[article.id].append([detail.word.word,
                                         detail.usage])
    template = 'stories/story.html'

    return render(request, template, {'story': story,
                                      'articles': articles,
                                      'wordDict': wordDict,
                                      'shared_words': shared_words})


def Storyviewbyyear(request, **kwargs):
    print kwargs
    return render(request, 'stories/index.html')
