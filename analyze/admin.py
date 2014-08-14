from django.contrib import admin
from analyze.models import FeedSource, ParseRule


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

admin.site.register(FeedSource, FeedSourceAdmin)
