# -*- coding: utf-8 -*-
from rest_framework import schemas

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from instanotifier.feedsource import urls as feedsource_urls


schema_view = schemas.get_schema_view(title="InstaNotifier stored notifications API", description="InstaNotifier stored notifications API")

urlpatterns = [
    url(r'^', include(feedsource_urls)),
    url(r'^feeds/', include(feedsource_urls)),
    url(r'^home/$', TemplateView.as_view(template_name='pages/home.html'), name='home'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^users/', include('instanotifier.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # API.v1
    url(r'^api-schema/', schema_view),
    url(r'^api/v1/', include('instanotifier.api.urls', namespace='api-v1')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
