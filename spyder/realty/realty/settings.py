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

DOWNLOAD_DELAY = 1.25
LOG_LEVEL = 'INFO'