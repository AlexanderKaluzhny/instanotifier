import json
import time
import calendar
from datetime import datetime

from django.core.serializers.json import DjangoJSONEncoder


class DateTimeIsoformat(datetime):
    """ Intended to replace default separator argument for isoformat method.
        Django forms.DateTimeField does not understand the u'2017-02-10T12:17:50' datetime format
    """

    def isoformat(self, sep=' '):
        """ calls the datetime.datetime.isoformat method with sep argument to be ' ' instead of 'T' """
        return super(DateTimeIsoformat, self).isoformat(sep)


class TimeAwareJsonSerializer(DjangoJSONEncoder):
    """ Json serializer that handles the Python time objects. """

    def default(self, o):
        """ get the time object, convert into datetime and pass to parent. """

        if isinstance(o, time.struct_time):
            r = calendar.timegm(o)
            o = DateTimeIsoformat.fromtimestamp(r)

        return super(TimeAwareJsonSerializer, self).default(o)


# Encoder function
def dumps(obj):
    return json.dumps(obj, cls=TimeAwareJsonSerializer)


# Decoder function
def loads(obj):
    return json.loads(obj)
