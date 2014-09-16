from django.conf.urls import patterns, url
from analyze import views


urlpatterns = patterns('',
   url(r'^$', views.Index, name='index'),
   url(r'^login', views.Login, name='login'),
   url(r'^logout$', views.Logout, name='logout'),
   url(r'^story/(?P<story>\w+)', views.Story, name='story'),
   url(r'^reassign', views.Reassign, name='reassign'),
   url(r'^delete', views.Delete, name='delete'),
   url(r'^worddelete', views.Worddelete, name='worddelete'),
   url(r'^testfeed/(?P<story>\w+)', views.Testfeedstory, name="testfeedstory"),
   url(r'^testfeed', views.Testfeedrss, name='testfeedrss')
)  # noqa
