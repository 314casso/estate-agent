# -*- coding: utf-8 -*-
from exportdata.engines.avito import AvitoEngine
from exportdata.models import FeedEngine


class FeedEngineFactory(object):
    FEEDENGINE_MAP = {
        FeedEngine.AVITO: AvitoEngine,
    }
    @staticmethod
    def get_feed_engine(feed):        
        return FeedEngineFactory.FEEDENGINE_MAP.get(feed.feed_engine.engine)(feed)
    