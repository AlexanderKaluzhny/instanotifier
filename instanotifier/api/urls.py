from django.conf.urls import url, include

from instanotifier.api.notification import views as notification_views


urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),

    url(r'^$', notification_views.NotificationListView.as_view(), name='rssnotification-list'),
]
