from django.shortcuts import render, reverse

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from instanotifier.feedsource.models import FeedSource
from instanotifier.feedsource.forms import FeedSourceForm


class FeedSourceListView(ListView):
    model = FeedSource
    template_name = "feedsource/feedsource_list.html"


class FeedSourceCreateUpdateMixin(object):
    model = FeedSource
    form_class = FeedSourceForm
    context_object_name = "feedsource"

    def get_success_url(self):
        return reverse("feedsource:list")


class FeedSourceCreateView(FeedSourceCreateUpdateMixin, CreateView):
    template_name = "feedsource/feedsource_create.html"


class FeedSourceUpdateView(FeedSourceCreateUpdateMixin, UpdateView):
    template_name = "feedsource/feedsource_update.html"
