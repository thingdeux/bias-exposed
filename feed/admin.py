from django.contrib import admin
from feed.models import Story, Feed, Word


class FeedInline(admin.StackedInline):
    model = Feed
    fields = (['source', 'title', 'url'])
    extra = 0


class StoryAdmin(admin.ModelAdmin):
    ordering = (['-post_date'])
    inlines = ([FeedInline])
    fields = ([('title', 'article_slug'), 'body', 'url', 'post_date'])
    list_display = (['title', 'article_slug', 'post_date'])
    search_fields = (['post_date'])


# Only creating for debugging - will create custom portal for viewing
# Due to the large amount of entries this will contain
class WordAdmin(admin.ModelAdmin):
    ordering = (['word'])
    list_display = (['word'])
    fields = (['word', 'feeds'])


admin.site.register(Story, StoryAdmin)
admin.site.register(Word, WordAdmin)
