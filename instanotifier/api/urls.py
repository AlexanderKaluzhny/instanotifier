from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from instanotifier.api.notification import views as notification_views

app_name = "api-v1"

router = DefaultRouter()
router.include_root_view = False

router.register(
    r'rss-search',
    notification_views.NotificationSearchViewSet,
    basename='rss'
)

urlpatterns = router.urls

urlpatterns += [
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
