from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^farhood/', include('farhoodapp.urls')),
    url('^', include('django.contrib.auth.urls')),
]