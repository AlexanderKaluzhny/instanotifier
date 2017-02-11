import json
import time
import calendar
from datetime import datetime

from django.core.serializers.json import DjangoJSONEncoder

class TimeAwareJsonSerializer(DjangoJSONEncoder):
    """ Json serializer that handles the Python time objects. """

    def default(self, o):
        """ get the time object, convert into datetime and pass to parent. """

        if isinstance(o, time.struct_time):
            r = calendar.timegm(o)
            o = datetime.fromtimestamp(r)

        return super(TimeAwareJsonSerializer, self).default(o)

# Encoder function
def dumps(obj):
    return json.dumps(obj, cls=TimeAwareJsonSerializer)

# Decoder function
def loads(obj):
    return json.loads(obj)
