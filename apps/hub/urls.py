"""URL path for user management on frontend."""

from django.urls import include, path

from apps.hub.views import (
    about,
    add_comment,
    contact,
    delete_comment,
    edit_marker,
    get_marker,
    home,
    like,
    privacy_policy,
    user_markers,
)

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("privacy-policy/", privacy_policy, name="privacy_policy"),
    path("contacts/", contact, name="contact"),
    path("markers/", user_markers, name="markers"),
    path("edit-marker/<int:marker_id>/", edit_marker, name="edit_marker"),
    path("marker/<int:marker_id>/", get_marker, name="get_marker"),
    path("like/", like, name="like"),
    path("add_comment/", add_comment, name="add_comment"),
    path("delete_comment/", delete_comment, name="delete_comment"),
]
