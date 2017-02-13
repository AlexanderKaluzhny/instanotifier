import hashlib

from django import forms
from instanotifier.notification.models import RssNotification


class RssNotificationForm(forms.ModelForm):
    # internal_id = forms.CharField(max_length=255)

    class Meta:
        model = RssNotification
        fields = ['entry_id', 'title', 'summary', 'link', 'published_parsed']  # , 'internal_id'

    def __init__(self, *args, **kwargs):
        super(RssNotificationForm, self).__init__(*args, **kwargs)
        if self.data and self.data.get('id', None):
            self.data.update(entry_id=self.data['id'])

    # def _post_clean(self):
    #     super(RssNotificationForm, self)._post_clean()
    #     cleaned_data = self.cleaned_data

    def get_instance_internal_id(self):
        internal_id = None
        id = self.cleaned_data.get('entry_id', None)
        if id:
            internal_id = self.instance.compute_internal_id(id)

        return internal_id
