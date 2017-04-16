from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='homepage.html'),
        name='homepage'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mcqs/', include('mcqs.urls', namespace='mcqs')),
    url(r'^coding/', include('coding.urls', namespace='coding')),
    url(r'^team/', include('teams.urls', namespace='teams')),
    url(r'^scores/', include('scores.urls', namespace='scores')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
