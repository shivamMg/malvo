from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^leaderboard/(?P<app>mcqs|coding)/$', views.leaderboard,
        name='leaderboard'),
    url(r'^evaluate/(?P<team_name>.*)/(?P<app>mcqs|coding)/$', views.evaluate,
        name='evaluate'),
]
