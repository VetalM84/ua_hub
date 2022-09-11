"""URL path for user management on frontend."""

from django.urls import include, path

from apps.hub.views import about, home, user_markers

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("markers/", user_markers, name="markers"),
]
