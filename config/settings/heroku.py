from .production import *  # noqa


# disable emailing, as long as mailgun is not connected to heroku
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_ALLOW_REGISTRATION = False
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

# Logging into console instead of mail_admins
LOGGING['loggers']['django.request']['handlers'] = ['console']
LOGGING['loggers']['general_file']['handlers'] = ['console']
LOGGING['handlers']['file'] = LOGGING['handlers']['console']

# disabled for test purposes
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_HTTPONLY = False

# there is no ElasticSearch deployed on Heroku
ELASTICSEARCH_DSL_AUTOSYNC = False
