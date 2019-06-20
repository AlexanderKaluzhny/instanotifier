from instanotifier.feedsource.models import FeedSource
from django import forms


class FeedSourceForm(forms.ModelForm):
    class Meta:
        model = FeedSource
        fields = "__all__"
