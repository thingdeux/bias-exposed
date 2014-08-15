from django.conf.urls import patterns, url
from feed import views


urlpatterns = patterns('',
   url(r'^$', views.Index, name='index'),
)  # noqa
