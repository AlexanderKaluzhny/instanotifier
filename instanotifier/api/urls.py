from django.conf.urls import url, include

from instanotifier.api.notification import views as notification_views


app_name = "api-v1"
urlpatterns = [
    url(
        r"^$",
        notification_views.NotificationListView.as_view(),
        name="rssnotification-list",
    ),
    # url(r'^notifications/(?P<pk>\d+)/rating/(?P<rating>[\w]+)$', notification_views.NotificationVotingView.as_view(), name='rssnotification-rating'),
    url(
        r"^notifications/rating/$",
        notification_views.NotificationVotingView.as_view(),
        name="rssnotification-rating",
    ),
    url(
        r"^dates/$",
        notification_views.NotificationDatesListView.as_view(),
        name="rssnotification-date-list",
    ),
]
