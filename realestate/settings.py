import os
import datetime
import socket

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
FILE_UPLOAD_PERMISSIONS = 0777

DEBUG = socket.gethostname() == 'picasso-kubuntu'
THUMBNAIL_DEBUG = DEBUG
PUBLIC_MEDIA_URL = "http://copy.domnatamani.ru"
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'db.domnatamani.ru', 'copy.domnatamani.ru']
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ADMINS = (
     ('Picasso', 'picasso75@yandex.ru'),
)

CORRECT_DELTA = datetime.datetime.now() -  datetime.timedelta(days=60)

MAX_CREDIT_MONTHS = 360
INTEREST_RATE = 9.5/100 
MAX_CREDIT_SUM = 0.1

from local_settings import * #@UnusedWildImport

LOGIN_REQUIRED_URLS = (
    r'/estatebase/(.*)$',    
    r'/devrep/(.*)$',
    r'/export/(.*)$',
)

LOGIN_REQUIRED_URLS_EXCEPTIONS = ('logon',)

LOGIN_REDIRECT_URL = '/estatebase/estatelist/'

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

USE_THOUSAND_SEPARATOR = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#ADMIN_MEDIA_PREFIX = '/static/admin/'

ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'd3lqzns@0$bz89skq@eroql^_1zx4prshdle^(aly!z^zwq5o('

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(SITE_ROOT, 'templates')],    
    'OPTIONS': {
        'loaders': [
            ('django.template.loaders.cached.Loader', [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]),
        ],
        'context_processors': [                
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
         ],
        'debug': DEBUG,
    },
}]


MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',                  
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'middleware.FilterPersistMiddleware',
    'django_sorting.middleware.SortingMiddleware',
    'middleware.RequireLoginMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
    'request.middleware.RequestMiddleware',    
)

PROFILE_LOG_BASE = MEDIA_ROOT

CSRF_FAILURE_VIEW = 'estatebase.views.csrf_failure'

ROOT_URLCONF = 'urls'

CACHES = {
    'default': dict(
        BACKEND = 'django.core.cache.backends.memcached.MemcachedCache',
        LOCATION = ['127.0.0.1:11211'],
    )
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',    
    'django.contrib.admin',    
    'estatebase',
    'sitetree',
    'orderedmodel',
    'selectable',    
    'django_sorting',
    'django.contrib.humanize',      
    'form_utils',  
    'wp_helper',
    'devrep',
    'sorl.thumbnail',
    'mptt',
    'spyder_helper',
    'exportdata',    
    'session_security',  
    'request',  
    'debug_toolbar', 
    'xmlrpc',   
)

PATH_TO_FONT = os.path.join(MEDIA_ROOT, 'verdana.ttf')
THUMBNAIL_ENGINE = 'watermarker.sorl_engine.WatermarkEngine'
WATERMARK_OPTIONS = {'font_scale': 0.04, 'font_path': PATH_TO_FONT, 'color': 'white', 'opacity': .8} # Any other options from watermark function
WATERMARK_MIN_SIZE = 50 #Minimum image size (max(height, width)) to add watermark
WATERMARK_FORCE = 'www.domnatamani.ru'

REQUEST_IGNORE_PATHS = (
    r'^estatebase/selectable/',
    r'^session_security/',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(SITE_ROOT, 'logs', 'logfile'),
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': True,
        },
        'estate': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
    }
}