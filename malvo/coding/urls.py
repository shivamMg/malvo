from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_no>[0-9]+)/$', views.challenge, name='challenge'),
]
