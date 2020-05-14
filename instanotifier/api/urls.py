from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from instanotifier.api.notification.search import NotificationSearchViewSet
from instanotifier.api.notification import endpoints

app_name = "api-v1"

router = DefaultRouter()

router.register(
    r'rss-search',
    NotificationSearchViewSet,
    basename='rss'
)
router.register(
    r'notifications',
    endpoints.NotificationViewSet,
    basename="notification"
)

urlpatterns = router.urls

urlpatterns += [
    url(
        r"^dates/$",
        endpoints.NotificationDatesListEndpoint.as_view(),
        name="rssnotification-date-list",
    ),
]
