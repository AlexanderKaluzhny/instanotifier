from django.utils.functional import cached_property
from instanotifier.notification.models import queryset_exclude_downvoted


class CheckboxExcludeDownvotedNotification(object):
    """ Manages the checkbox for displaying whether the downvoted notifications are excluded from list.
        Provides an url to include the downvoted notifications into listing.
    """
    @property
    def url(self):
        url = getattr(self, '_url', '')
        assert len(url), "url for getting of queryset including downvoted notifications is not evaluated."
        return url

    @property
    def is_checked(self):
        is_checked = getattr(self, '_is_checked', None)
        assert is_checked is not None, "checked attribute is not set, yet."
        return is_checked

    def set_checked(self, value, view):
        self._is_checked = value
        self._url = self.build_url(view, include_all=value)

    @classmethod
    def build_url(self, view, include_all=False):
        """ Build url to be able to get queryset including downvoted notifications """
        from django.http.request import iri_to_uri

        full_path = view.request._request.get_full_path()
        current_query_params = view.request.query_params.copy()
        # strip query params from full_path
        full_path_no_params = full_path.split("?")[0]

        # remove pagination param from query params
        page_num = None
        if view.pagination_class and current_query_params.get(view.pagination_class.page_query_param, None):
            page_num = current_query_params.pop(view.pagination_class.page_query_param)

        if include_all:
            current_query_params['include_rating'] = 'all'
        elif 'include_rating' in current_query_params:
            current_query_params.pop('include_rating')

        query_params_urlencoded = current_query_params.urlencode()

        output_full_path = '%s%s' % (
            full_path_no_params,
            ('?' + iri_to_uri(query_params_urlencoded)) if query_params_urlencoded else ''
        )
        return output_full_path


class RatingManager(object):
    """ Manages the rating logic for RssNotifications """

    @cached_property
    def checkbox(self):
        return CheckboxExcludeDownvotedNotification()

    def filter_queryset(self, request, queryset, view):
        self.checkbox.is_shown = True

        # skip custom filtering of downvoted if explicitly filter by 'rating'
        if 'rating' in request.query_params:
            self.checkbox.is_shown = False
            return queryset

        # don't filter by rating if '?include_rating=all' specified
        include_all = request.query_params.get('include_rating', None)
        if include_all and include_all == 'all':
            self.checkbox.set_checked(False, view)
            return queryset

        queryset = queryset_exclude_downvoted(queryset)
        self.checkbox.set_checked(True, view)
        return queryset
