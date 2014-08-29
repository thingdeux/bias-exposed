from django.conf.urls import patterns, url
from stories import views


urlpatterns = patterns('',
   url(r'^$', views.Index, name='index'),
)  # noqa
