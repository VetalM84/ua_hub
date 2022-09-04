"""URL path for user management on frontend."""

from django.urls import path, include

from apps.hub.views import home

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("", home, name="home"),
]
