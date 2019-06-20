import hashlib

from django import forms
from instanotifier.notification.models import RssNotification


class RssNotificationForm(forms.ModelForm):
    class Meta:
        model = RssNotification
        fields = ["entry_id", "title", "summary", "link", "published_parsed"]

    def __init__(self, *args, **kwargs):
        super(RssNotificationForm, self).__init__(*args, **kwargs)
        if self.data and self.data.get("id", None):
            self.data.update(entry_id=self.data["id"])
