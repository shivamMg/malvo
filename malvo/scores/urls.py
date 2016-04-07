from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^lb/(?P<app>mcqs|coding)/$', views.leaderboard,
        name='leaderboard'),
    url(r'^eval/(?P<team_name>.*)/(?P<app>mcqs|coding)/$', views.evaluate,
        name='evaluate'),
    url(r'^display_file/(?P<team_name>.*)/(?P<question_no>[0-9]+)/$', views.display_file,
        name='display_file'),
]
