from django.conf.urls import url

from instanotifier.feedsource import views

app_name = "feedsource"

urlpatterns = [
    url(regex=r"^$", view=views.FeedSourceListView.as_view(), name="list"),
    url(
        regex=r"^update/(?P<pk>\d+)/$",
        view=views.FeedSourceUpdateView.as_view(),
        name="update",
    ),
    url(regex=r"^create/$", view=views.FeedSourceCreateView.as_view(), name="create"),
]
