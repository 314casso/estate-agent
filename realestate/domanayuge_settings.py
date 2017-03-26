from settings import * #@UnusedWildImport
SITE_ID = 2
ROOT_URLCONF = 'domanayuge.urls'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.domanayuge.ru', 'domanayuge.ru', 'www.domanayuge.ru']

CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'

STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
STATIC_URL = '/static/'

WATERMARK_FORCE = None

ROOT_HOSTCONF = 'domanayuge.hosts'
DEFAULT_HOST = 'www'

if DEBUG:
    PARENT_HOST = 'localhost:8000'
else:
    PARENT_HOST = 'domanayuge.ru'

MIDDLEWARE_CLASSES = (
    'django_hosts.middleware.HostsRequestMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',                  
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'middleware.FilterPersistMiddleware',
    'django_sorting.middleware.SortingMiddleware', 
    'django_hosts.middleware.HostsResponseMiddleware',     
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
    'django_hosts',
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