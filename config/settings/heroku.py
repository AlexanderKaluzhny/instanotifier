from __future__ import absolute_import, unicode_literals

from .production import *  # noqa


# disable emailing, as long as mailgun is not connected to heroku
ACCOUNT_EMAIL_VERIFICATION = 'none'
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

# Logging into console instead of mail_admins
LOGGING['loggers']['django.request']['handlers'] = ['console']
