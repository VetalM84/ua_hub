"""URL path for user management on frontend."""

from django.urls import path

from apps.hub.views import home

urlpatterns = [
    path("", home, name="home"),
]
