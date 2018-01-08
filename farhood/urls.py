from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from farhood import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^farhood/', include('farhoodapp.urls')),
    url('^', include('django.contrib.auth.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
