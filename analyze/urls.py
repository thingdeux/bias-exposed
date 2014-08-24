from django.conf.urls import patterns, url
from analyze import views


urlpatterns = patterns('',
   url(r'^$', views.Index, name='index'),
   url(r'^story/(?P<story>\w+)', views.Story, name='story'),
   url(r'^reassign', views.Reassign, name='reassign'),
   url(r'^delete', views.Delete, name='delete'),
   url(r'^deleteword', views.Delete_Word_Detail, name='delete word')
)  # noqa
