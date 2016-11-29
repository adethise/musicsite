from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^random$', views.random, name='random'),
        url(r'^(?P<song_id>[0-9]+)$', views.song, name='song')
]
