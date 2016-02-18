from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^mcq/$', views.mcq, name='mcq'),
    url(r'^(?P<question_no>[0-9]+)/answer/$', views.answer, name='answer'),
]
