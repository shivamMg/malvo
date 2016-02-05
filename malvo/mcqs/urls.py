from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.McqView.as_view(), name='mcq'),
    url(r'^(?P<question_no>[0-9]+)/answer/$', views.answer, name='answer'),
]
