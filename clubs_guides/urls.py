from django.conf.urls import url

from clubs_guides.views import (
    ClubsGuidesListView,
    ClubsGuideView,
    CategoryListView,
)


urlpatterns = [
    url("^$", ClubsGuidesListView.as_view(), name="clubsguide-list"),
    url(r"^(?P<pk>[0-9]+)", ClubsGuideView.as_view(), name="clubsguide"),
    url(
        "^categories",
        CategoryListView.as_view(),
        name="clubsguide-category-list"
    ),
]
