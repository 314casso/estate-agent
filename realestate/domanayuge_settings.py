from settings import * #@UnusedWildImport
SITE_ID = 1
ROOT_URLCONF = 'domanayuge.urls'
DEBUG = True

CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'

STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
STATIC_URL = '/static/'

WATERMARK_FORCE = None

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',                  
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'middleware.FilterPersistMiddleware',
    'django_sorting.middleware.SortingMiddleware',      
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',    
    'django.contrib.admin',   
    'django.contrib.humanize',
    'django_markwhat',
    'orderedmodel',    
    'categories.editor',
    'content_edit',      
    'form_utils', 
    'sorl.thumbnail',
    'selectable',
    'mptt',   
    'estatebase',
    'devrep',
    'domanayuge',
)