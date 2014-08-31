from django.conf.urls import patterns, url
from stories import views


urlpatterns = patterns('',
   url(r'^$', views.Index, name='index'),
   # View All stories in a given year
   # (ex: stories/2004/ would bring up all stories in 2014)
   url(r'^stories/(?P<year>[0-9]{4})/$', views.Storyviewbyyear, name='story_view_by_year'),
   url(r'^stories/(?P<slug>.*)', views.Storybyslug, name='story_view_by_slug'),

)  # noqa
