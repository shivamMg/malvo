from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(
        r'^login/',
        auth_views.login,
        name='login',
        kwargs={'template_name': 'teams/login.html'},
    ),
    url(
        r'^logout/',
        auth_views.logout,
        name='logout',
        kwargs={'next_page': '/'},
    ),
    url(
        r'^register/',
        views.register_team,
        name='register',
    ),
    url(r'^profile/$', views.profile, name='profile'),
]
