"""URL path for user management on frontend."""

from django.urls import include, path

from apps.hub.views import about, home

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("", home, name="home"),
    path("about/", about, name="about"),
]
