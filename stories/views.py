from django.shortcuts import render
from stories.models import Story, Article, Word, Detail


def Index(request):
    stories = Story.objects.all()
    return render(request, 'stories/index.html', {'stories': stories})


def Storybyslug(request, **kwargs):
    slug_query = kwargs['slug']
    story = Story.objects.get(article_slug=slug_query)
    articles = Article.objects.filter(story=story).select_related()
    word_details = Detail.objects.filter(article__story=story).select_related()
    shared_words = story.shared_words.split('|')

    return render(request, 'stories/story.html', {'story': story,
                                                  'articles': articles,
                                                  'word_details': word_details,
                                                  'shared_words': shared_words})

def Storyviewbyyear(request, **kwargs):
    print kwargs
    return render(request, 'stories/index.html')
