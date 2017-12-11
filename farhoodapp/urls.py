from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/user/$', views.UserCreate.as_view()),
]