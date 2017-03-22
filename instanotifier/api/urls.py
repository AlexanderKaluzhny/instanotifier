from django.conf.urls import url, include

from instanotifier.api.notification import views as notification_views


urlpatterns = [
    url(r'^$', notification_views.NotificationListView.as_view(), name='rssnotification-list'),
    url(r'^dates/$', notification_views.NotificationDatesListView.as_view(), name='rssnotification-date-list'),
]
