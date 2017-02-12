import hashlib

from django import forms
from instanotifier.notification.models import RssNotification


class RssNotificationForm(forms.ModelForm):
    """ The form for validation and creation of the RssNotification instances. """
    class Meta:
        model = RssNotification
        fields = ['id', 'title', 'summary', 'link', 'published_parsed'] # , 'internal_id'

    def __init__(self, *args, **kwargs):
        super(RssNotificationForm, self).__init__(*args, **kwargs)

    def _post_clean(self):
        super(RssNotificationForm, self)._post_clean()
        cleaned_data = self.cleaned_data

        id = cleaned_data.get('id')
        self.internal_id = self.instance.compute_internal_id(id)
        # what is the value of instance.internal_id now ?

