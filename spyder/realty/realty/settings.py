# Scrapy settings for realty project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
BOT_NAME = 'realty'

SPIDER_MODULES = ['realty.spiders']
NEWSPIDER_MODULE = 'realty.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'realty (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'realty.pipelines.RealtyPipeline': 300,    
}

USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 4.0; obot)'
DOWNLOAD_DELAY = 5
LOG_LEVEL = 'INFO'

from realty.local_settings import DJANGO_PATHES
import sys
sys.path.extend(DJANGO_PATHES)
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

def setup_django_env(path):
    import imp
    from django.core.management import setup_environ
    f, filename, desc = imp.find_module('settings', [path])
    project = imp.load_module('settings', f, filename, desc)     
    setup_environ(project)
setup_django_env(DJANGO_PATHES[0])