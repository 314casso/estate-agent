# -*- coding: utf-8 -*-
from exportdata.engines.avito import AvitoEngine
from exportdata.models import FeedEngine
from exportdata.engines.yandex import YandexEngine
from exportdata.engines.wp import WPEngine
from exportdata.engines.sitebill import Sitebill


class FeedEngineFactory(object):
    FEEDENGINE_MAP = {
        FeedEngine.AVITO: AvitoEngine,
        FeedEngine.YANDEX: YandexEngine,
        FeedEngine.WP: WPEngine,
        FeedEngine.SITEBILL: Sitebill
    }
    
    @staticmethod
    def get_feed_engine(feed):        
        return FeedEngineFactory.FEEDENGINE_MAP.get(feed.feed_engine.engine)(feed)
    