"""URL path for user management on frontend."""

from django.urls import include, path

from apps.hub.views import about, edit_marker, home, user_markers

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("markers/", user_markers, name="markers"),
    path("edit-marker/<int:marker_id>", edit_marker, name="edit_marker"),
]
