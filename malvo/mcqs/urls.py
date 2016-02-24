from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^mcq/$', views.mcq, name='mcq'),
    url(r'^answer/$', views.answer, name='answer'),
]
