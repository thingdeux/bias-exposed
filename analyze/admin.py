from django.contrib import admin
from analyze.models import FeedSource, ParseRule
from analyze.models import PotentialStory, PotentialArticle


class ParseRuleInline(admin.StackedInline):
    model = ParseRule
    fields = (['dom_selector', 'caused_error'])
    # This should only be released programmatically upon succesful feed pull
    readonly_fields = (['caused_error'])
    extra = 0


class FeedSourceAdmin(admin.ModelAdmin):
    ordering = (['source'])
    inlines = [ParseRuleInline]
    list_display = (['source', 'rss_feed_url'])
    fields = (['source', 'rss_feed_url'])
    search_fields = (['source'])


class PotentialArticleInline(admin.StackedInline):
    verbose_name = "Potential Article Match"
    verbose_name_plural = "Potential Article Matches"
    ordering = ['source', '-final_match_score']
    model = PotentialArticle
    """ --For Debug
    fields = (['title', 'url',
               ('match_title', 'match_body',
                'match_quotes', 'match_sentences'), 'match_key'])
    """
    fields = (['title', 'url'])

    readonly_fields = (['source', 'title', 'final_match_score', 'url'])
    extra = 0


class PotentialStoryAdmin(admin.ModelAdmin):
    inlines = [PotentialArticleInline]
    fields = (['title', 'to_publish'])
    list_display = (['title', 'to_publish'])


class PotentialArticleAdmin(admin.ModelAdmin):
    fields = (['potentialstory', 'title'])


admin.site.register(FeedSource, FeedSourceAdmin)
admin.site.register(PotentialStory, PotentialStoryAdmin)
admin.site.register(PotentialArticle, PotentialArticleAdmin)
