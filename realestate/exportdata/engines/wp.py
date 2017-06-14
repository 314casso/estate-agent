# -*- coding: utf-8 -*-
from lxml import etree
from exportdata.engines.base import BaseEngine
from exportdata.mappers.base import BaseMapper
import pytz


tz = pytz.timezone('Europe/Moscow')


class WPEngine(BaseEngine):
    VERSION = '1.0' 
    def get_XHTML(self, lots, use_cache):
        self._use_cache = use_cache     
        xhtml = etree.Element('lots')
        xhtml.set("target", 'wordpress')
        xhtml.set("formatVersion", self.VERSION)
        self.add_offers(xhtml, lots)
        return xhtml
    
    def create_offer(self, lot):
        mapper = WPMapper(lot, self._feed)                
        empty_nodes = []  
        errors = {}  
        warnings = {}   
        offer = etree.Element("lot")
        el_maker = self.el_maker(offer, empty_nodes)
        el_maker("id", mapper.id)
        el_maker("state", mapper.validity_state)
        el_maker("status", mapper.estate_status)
        el_maker("updated", mapper.last_update_date)
        
        if len(empty_nodes):
            errors['empty_nodes'] = u', '.join(empty_nodes)
                   
        return (offer, {'errors': errors, 'warnings': warnings})
        

def xml_date(date):        
    return tz.localize(date).replace(microsecond=0).isoformat()


class WPMapper(BaseMapper):
    _modificated = None
    _validity_state = None
    _last_update_date = None
    _estate_status = None
    @property    
    def validity_state(self):
        if not self._validity_state:
            self._validity_state = u'%s' % self._estate.validity_state           
        return self._validity_state    
    
    @property    
    def estate_status(self):
        if not self._estate_status:
            self._estate_status = u'%s' % self._estate.estate_status           
        return self._estate_status    
        
    @property
    def last_update_date(self):        
        if not self._last_update_date:
            self._last_update_date = xml_date(self._estate.history.modificated) 
        return self._last_update_date
    