from django.conf.urls import patterns, url
from analyze import views


urlpatterns = patterns('',
   url(r'^$', views.Index, name='index'),
   url(r'^story/(?P<story>\w+)', views.Story, name='story')
)  # noqa
