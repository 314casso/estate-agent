# -*- coding: utf-8 -*-
from estatebase.models import EstateTypeCategory, EstateType, Locality,\
    WallConstrucion, EstateParam, EntranceEstate, Interior
from exportdata.models import ValueMapper
import re
from django.core.cache import cache
from django.template import loader
from django.template.context import Context
from django.template.defaultfilters import striptags
from django.contrib.contenttypes.models import ContentType
import hashlib
import os
import logging
from django.utils.encoding import smart_unicode
import pytz
from exportdata.utils import EstateTypeMapper, ApplianceMapper

logger = logging.getLogger('estate')
tz = pytz.timezone('Europe/Moscow')

def number2xml(d):
    return '%.12g' % d if d else ''

def xml_date(date):        
    return tz.localize(date).replace(microsecond=0).isoformat()

class BaseMapper(object):
    _id = None
    _description = None  
    _living_space = None  
    _area = None
    _land_area = None
    _floor = None
    _floors = None
    _category = None
    _object_type = None
    _estate_type_id = None
    _rooms = None
    
    def __init__(self, estate, feed):
        self._estate = estate
        self._basic_bidg = estate.basic_bidg
        self._basic_stead = self._estate.basic_stead                
        self._layout = None
        self._price = self.Price(estate)      
        self._address = self.Address(estate, self, feed)
        self._contact = self.Contact(estate, feed)
        self._feed = feed
        self._domain = 'http://%s' % 'feed.domnatamani.ru'
        if self._basic_bidg:
            self._estate_type_id = self._basic_bidg.estate_type_id
        elif self._basic_stead:
            self._estate_type_id = self._basic_stead.estate_type_id
            
    
    @property    
    def id(self):
        if not self._id:
            self._id = u'%s' % self._estate.id           
        return self._id 
    
    @property
    def object_type(self):
        if not self._object_type:                                     
            if self._estate_type_id:                
                self._object_type = self.get_value_mapper(EstateType, self._estate_type_id, 'ObjectType')
        return self._object_type
    
    
    class Contact:
        _office = None
                
        def __init__(self, estate, feed):
            self._feed = feed
            self._campaign = feed.campaign
            self._estate = estate          
                    
        @property
        def office(self):
            if not self._office:
                self._office = self._estate.region.office_set.all()[:1].get()
            return self._office
    
        @property
        def manager_name(self):    
            if self._feed.use_broker and self._estate.broker and self._estate.broker.first_name:
                return u'%s' % self._estate.broker.first_name          
            if self._campaign and self._campaign.valid and self._campaign.person:
                return u'%s' % self._campaign.person     
            return u'%s' % self.office.head.first_name
    
        @property
        def email(self):    
            if self._campaign and self._campaign.valid and self._campaign.email:
                return u'%s' % self._campaign.email     
            return u'pochta@domana_lot_manageryuge.ru'
         
        @property
        def phone(self):
            if self._feed.use_broker and self._estate.broker and self._estate.broker.userprofile.phone:
                return u'%s' % self._estate.broker.userprofile.phone            
            if self._campaign and self._campaign.valid and self._campaign.phone:
                return u'%s' % self._campaign.phone     
            return u'%s' % self._office.head.userprofile.phone

        
    def get_value_mapper(self, model_class, object_id, xml_node):
        cache_key = hashlib.md5(("%s%s%s%s" % (model_class, object_id, xml_node, self._feed.feed_engine))).hexdigest()                                               
        xml_value = cache.get(cache_key)        
        if xml_value is not None:            
            return smart_unicode(xml_value)
        try:
            value_mapper = ValueMapper.objects.get(content_type=ContentType.objects.get_for_model(model_class), object_id=object_id, 
                                                   mapped_node__xml_node=xml_node, mapped_node__type_mapper__feed_engine=self._feed.feed_engine)
            xml_value = value_mapper.xml_value
            cache.set(cache_key, xml_value, 300)
            return xml_value             
        except ValueMapper.DoesNotExist:
            return
    
    @property
    def rooms(self):
        return number2xml(self.get_rooms())
      
    def get_rooms(self):
        if not self._rooms: 
            if self._basic_bidg:
                self._rooms = self._basic_bidg.room_count
        return self._rooms
            
    @property
    def price(self):
        return self._price
    
    @property
    def contact(self):
        return self._contact
    
    @property
    def address(self):
        return self._address
    
    class Address:      
        _city = None  
        _district = None    
        _street = None
        _bld_number = None
        _distance_to_city = None 
        _metropolis = None
        _restricted_street = None
        _microdistrict = None
        
        def __init__(self, estate, parent, feed):
            self._estate = estate
            self._parent = parent
            self._feed = feed
                
        @property
        def locality(self):
            if not self._city:
                if self._estate.locality:
                    self._city = u'%s %s' % (self._estate.locality.name, self._estate.locality.locality_type.sort_name)
            return self._city
        
        @property
        def metropolis(self):
            if not self._metropolis:
                self._metropolis = u'%s' % self._estate.region.metropolis
            return self._metropolis            
        
        @property    
        def district(self):
            if not self._district:
                self._district = self._estate.region.regular_name
            return self._district
        
        @property    
        def microdistrict(self):
            if not self._microdistrict:
                microdistrict = self._estate.microdistrict
                if microdistrict:
                    self._microdistrict = microdistrict.name
            return self._microdistrict
                
        def possible_street(self):
            if not self._estate.street:                
                return self.microdistrict or ''
            if not self._street:
                self._street = u'%s %s' % (self._estate.street.name, self._estate.street.street_type or '')
            return self._street
        
        def restricted_street(self):            
            if not self._restricted_street:
                if self._estate.locality and self._estate.street:                                
                    if self._estate.locality.locality_type_id == Locality.CITY and self._estate.estate_category_id == EstateTypeCategory.KVARTIRA:               
                        self._restricted_street = u'%s %s' % (self._estate.street.name, self._estate.street.street_type or '')
            return self._restricted_street
        
        @property
        def street(self):
            if self._feed.use_possible_street:
                return self.possible_street()
            return self.restricted_street()
        
        @property
        def bld_number(self):
            if not self._bld_number:
                self._bld_number = self._estate.estate_number
            return self._bld_number
        
        @property
        def distance_to_city(self):
            if not self._distance_to_city:
                self._distance_to_city = u'0'
            return self._distance_to_city
        
        @property    
        def country(self):
            return u'Россия'
        
        @property
        def region(self):
            return u'Краснодарский край'
    
    class Price:
        _value = None
        def __init__(self, estate):
            self._estate = estate
        @property     
        def value(self):
            if not self._value:
                self._value = re.sub(r'\s', '', str(self._estate.agency_price))
            return self._value
        
    def render_content(self, estate, description, short=False):        
        t = loader.get_template('reports/feed/text_content.html')
        c = Context({'estate_item':estate, 'description': description, 'short': short})
        rendered = t.render(c)
        return re.sub(r"\s+"," ", rendered).strip()
    
    def render_post_description(self, estate):
        if not estate.locality:
            return
        region = u'Краснодарского края' if estate.locality.locality_type_id == Locality.CITY else estate.locality.region.regular_name_gent
        location = u'%s %s' % (estate.locality.name_loct, region)
        result = u'Продается %s в %s' % (estate.estate_type.lower(), location)             
        return result
    
    @property        
    def description(self):
        if not self._description:
            description = self.render_post_description(self._estate)        
            return striptags(self.render_content(self._estate, description))
        return self._description
    
    @property
    def living_space(self):
        # жилая площадь (при продаже комнаты — площадь комнаты)
        if not self._living_space:
            if self._basic_bidg:             
                self._living_space = number2xml(self._basic_bidg.used_area)            
        return self._living_space       
    
    @property
    def area(self):
        # общая площадь
        if not self._area:
            if self._basic_bidg:             
                self._area = number2xml(self._basic_bidg.total_area)            
        return self._area
        
    @property
    def land_area(self):
        if not self._land_area:        
            if self._basic_stead:
                self._land_area = number2xml(self._basic_stead.total_area_sotka or '')
        return self._land_area
    
    @property
    def floor(self):
        if not self._floor:
            if self._basic_bidg:
                self._floor = number2xml(self._basic_bidg.floor)
        return self._floor
    
    @property
    def floors(self):
        if not self._floors:
            if self._basic_bidg:
                floor_count = self._basic_bidg.floor_count
                if floor_count is not None:
                    self._floors = number2xml(int(floor_count))
        return self._floors
        
    def images(self, max_images, clear_watermark=True):        
        from urlparse import urljoin       
        from sorl.thumbnail import get_thumbnail              
        images = self._estate.images.all()[:max_images]
        if images:
            result = []
            for img in images:
                try:               
                    im = get_thumbnail(img.image.file, '800x600', clear_watermark=clear_watermark)
                    head, tail = os.path.split(im.name)  # @UnusedVariable                                
                    result.append(urljoin(self._domain, im.url))                  
                except:
                    logger.debug('Wrong image file %s, lot %s!' % (img.image.file, img.estate))                    
            return result       

class AvitoMapper(BaseMapper):  
    _title = None
    _house_type = None
    _walls_type = None
    _market_type = None
        
    @property
    def category(self):
        if not self._category:
            self._category = self.get_category()
        return self._category
    
    def get_category(self):
        cat_id = self._estate.estate_category_id
        if cat_id == EstateTypeCategory.KVARTIRA and self._basic_bidg is not None:                                                        
            category = self.get_value_mapper(EstateType, self._estate_type_id, 'ObjectType')
            if category:
                return category             
        return self.get_value_mapper(EstateTypeCategory, cat_id, 'Category')
                     
    class Price(BaseMapper.Price):
        @property    
        def type(self):
            return u'за всё'
    
    class Address(BaseMapper.Address):    
        @property
        def city(self):
            if not self._city:
                self._city = self._parent.get_value_mapper(Locality, self._estate.locality_id, 'City')
            return self._city

    
    @property
    def title(self):
        if not self._title:
            self._title = self._estate.estate_category.name
        return self._title

    @property
    def house_type(self):
        if not self._house_type:
            if self._basic_bidg:                
                self._house_type = self.get_value_mapper(WallConstrucion, self._basic_bidg.wall_construcion_id, 'HouseType')
        return self._house_type            
    
    @property
    def walls_type(self):
        if not self._house_type:
            if self._basic_bidg:                
                self._house_type = self.get_value_mapper(WallConstrucion, self._basic_bidg.wall_construcion_id, 'WallsType')
        return self._house_type
         
    @property
    def market_type(self):
        if not self._market_type:
            self._market_type = u'Вторичка'
        return self._market_type
      
    @property
    def operation_type(self):        
        return u'Продам'
    
    @property
    def ad_status(self):
        return u'Free'
        
    @property
    def allow_email(self):
        return u'Да'
    
    @property
    def area(self):
        min_value = 20        
        if not self._area:
            if self._basic_bidg:             
                total_area = self._basic_bidg.total_area
                if total_area: 
                    self._area = number2xml(total_area if total_area > min_value else min_value)            
        return self._area

class YandexMapper(BaseMapper):
    _url = None
    _creation_date = None
    _last_update_date = None
    _mortgage = None
    _rooms_space = None
    _kitchen_space = None
    _renovation = None
    _quality = None
    _lot_type = None
    _new_flat = None
    _studio = None
    _apartments = None
    _rooms_type = None   
    _phone = None
    _internet = None
    _kitchen_furniture = None
    _room_furniture = None   
    _balcony = None
    _bathroom_unit = None
    _floor_covering = None
    _window_view = None
    _heating_supply = None
    _water_supply = None
    _sewerage_supply = None
    _electricity_supply = None
    _gas_supply = None
    _building_type = None
    _building_name = None
    _yandex_building = None 
    _yandex_building_id = None
    _built_year = None
    _ready_quarter = None
    _building_state = None
    _lift = None
    _ceiling_height = None
    _deal_status = None
    _suburban = None
    
    def bool_to_xml(self, bool_value):
        return u'да' if bool_value else u'нет'
    
    def bool_or_null(self, bool_value):
        if bool_value:
            return self.bool_to_xml(bool_value)       
    
    @property
    def category(self):
        if not self._category:
            self._category = self.get_category()
        return self._category
    
    @property
    def url(self):
        if not self._url:
            if self._estate.wp_meta:
                self._url = u'http://www.domnatamani.ru/?p=%s' % self._estate.wp_meta.post_id
        return self._url
    
    @property
    def creation_date(self):
        if not self._creation_date:
            self._creation_date = xml_date(self._estate.history.created) 
        return self._creation_date
    
    @property
    def last_update_date(self):        
        if not self._last_update_date:
            self._last_update_date = xml_date(self._estate.history.modificated) 
        return self._last_update_date
    
    def get_category(self):
        cat_id = self._estate.estate_category_id
        if cat_id == EstateTypeCategory.KVARTIRA and self._basic_bidg is not None:                                                        
            category = self.get_value_mapper(EstateType, self._estate_type_id, 'ObjectType')
            if category:
                return category             
        return self.get_value_mapper(EstateTypeCategory, cat_id, 'Category')
    
    def get_appliances(self, appliance_id):
        attr = '%s_%s' % ('appliance', appliance_id)
        result = getattr(self, attr, None)
        if not result:
            if self._basic_bidg:            
                result = self.bool_or_null(self._basic_bidg.appliances.filter(id=appliance_id))
                setattr(self, attr, result)
        return result
    
    @property
    def type(self):        
        return u'продажа' 
    
    @property
    def property_type(self):
        return u'жилая' 
    
    @property
    def suburban(self):
        if not self._suburban:
            self._suburban = (not self._estate.locality.locality_type_id == Locality.CITY) or (self._estate.estate_category_id == EstateTypeCategory.U4ASTOK)
        return self._suburban
    
    class Address(BaseMapper.Address):
        _microdistrict = None   
        @property
        def locality(self):
            if not self._city:
                if self._estate.locality:
                    self._city = u'%s' % (self._estate.locality.name)
            return self._city
        
        @property
        def sub_locality(self):
            if not self._microdistrict:        
                microdistrict = self._estate.microdistrict
                if microdistrict is not None:          
                    self._microdistrict = u'%s' % self._estate.microdistrict
            return self._microdistrict
                         
        def possible_street(self):
            # base function according schema
            if not self._street:
                if self._estate.street:
                    bld_number = ''            
                    if self._feed.show_bld_number and self._estate.locality.locality_type_id == Locality.CITY and self._estate.estate_number and self._estate.estate_category_id == EstateTypeCategory.KVARTIRA:                
                        bld_number = u", %s" % self._estate.estate_number
                    self._street = u'%s %s%s' % (self._estate.street.name, self._estate.street.street_type or '', bld_number)
            return self._street

     
    class Contact(BaseMapper.Contact):
        _category = None
        _organization = None
        _url = None

        @property
        def category(self):
            if not self._category:
                self._category = u'агентство' 
            return self._category
        
        @property
        def organization(self):
            if not self._organization:
                self._organization = u'Дома на юге - недвижимость и строительство' 
            return self._organization

        @property
        def url(self):
            if not self._url:
                self._url = u'http://www.domnatamani.ru/' 
            return self._url
    
    class Price(BaseMapper.Price):      
        @property    
        def currency(self):
            return u'RUB'
    
    @property
    def mortgage(self):
        '''
        возможность ипотеки
        '''
        if not self._mortgage:
            if len(self._estate.estate_params.filter(pk=EstateParam.IPOTEKA)) > 0:
                self._mortgage = self.bool_to_xml(True)
        return self._mortgage
    
    @property
    def deal_status(self):
        if not self._deal_status:
            self._deal_status = u'%s' % self._estate.deal_status if self._estate.deal_status else u'прямая продажа'
        return self._deal_status
       
    @property
    def rooms_space(self):
        if not self._rooms_space: 
            if self._basic_bidg:
                self._rooms_space = [number2xml(x) for x in self._basic_bidg.get_rooms_area()]
        return self._rooms_space  
    
    @property
    def kitchen_space(self):
        if not self._kitchen_space:
            if self._basic_bidg:       
                self._kitchen_space = number2xml(self._basic_bidg.get_kuhnya_area())
        return self._kitchen_space
    
    @property
    def renovation(self):
        if not self._renovation:
            # TODO: admin Interior
            if self._basic_bidg:
                self._renovation = self.get_value_mapper(Interior, self._basic_bidg.wall_construcion_id, 'Renovation')
        return self._renovation
            
    @property
    def quality(self):
        if not self._quality:
            # TODO: admin Interior
            if self._basic_bidg:
                self._quality = self.get_value_mapper(Interior, self._basic_bidg.wall_construcion_id, 'Quality')
        return self._quality        
    
    @property
    def lot_type(self):
        if not self._lot_type:
            self._lot_type = self._estate.estate_type
        return self._lot_type
        
    @property
    def new_flat(self):
        if not self._new_flat:        
            if self._basic_bidg:                
                self._new_flat = self.bool_or_null(self._estate_type_id == EstateTypeMapper.NOVOSTROYKA)
        return self._new_flat 
    
    @property
    def studio(self):
        if not self._studio:        
            if self._basic_bidg:
                self._studio = self.bool_or_null(self._estate_type_id == EstateTypeMapper.KVARTIRASTUDIYA)
        return self._studio

    @property
    def apartments(self):
        if not self._apartments:        
            if self._basic_bidg:
                self._apartments = self.bool_or_null(self._estate_type_id == EstateTypeMapper.APPARTAMENTY)
        return self._apartments
    
    @property
    def rooms_type(self):
        if not self._rooms_type:
            room_smezh = self._basic_bidg.get_room_smezh()
            room_izol = self._basic_bidg.get_room_izol()
            if room_smezh > 0 or room_izol > 0:
                if room_smezh > room_izol:
                    self._rooms_type = u'смежные'
                else:
                    self._rooms_type = u'раздельные'
        return self._rooms_type
    
    @property
    def phone(self):                
        CONNECTED = 3
        if not self._phone:        
            self._phone = self.bool_or_null(self._estate.telephony_id == CONNECTED)                
        return self._phone
    
    @property                
    def internet(self):
        CONNECTED = 3      
        if not self._internet:  
            self._internet = self.bool_or_null(self._estate.internet_id == CONNECTED)
        return self._internet
    
    @property   
    def kitchen_furniture(self):
        if not self._kitchen_furniture:
            if self._basic_bidg:
                self._kitchen_furniture = self.bool_or_null(self._basic_bidg.get_kitchen_furniture())
        return self._kitchen_furniture       
    
    @property
    def room_furniture(self):
        if not self._room_furniture:
            if self._basic_bidg:
                self._room_furniture = self.bool_or_null(self._basic_bidg.get_room_furniture())        
        return self._room_furniture     
    
    @property
    def television(self):
        return self.get_appliances(ApplianceMapper.TELEVIZOR)
    
    @property
    def washing_machine(self):
        return self.get_appliances(ApplianceMapper.STIRALNAYAMASHINA)        
    
    @property
    def refrigerator(self):
        return self.get_appliances(ApplianceMapper.HOLODILNIK)        
    
    @property
    def air_conditioner(self):
        return self.get_appliances(ApplianceMapper.KONDITSIONER)
        
    @property
    def ventilation(self):
        return self.get_appliances(ApplianceMapper.VENTILYATORY)
    
    def _supply(self, true_ids, no_id, fk):                         
            if fk == no_id:
                return self.bool_to_xml(False)
            else:
                return self.bool_or_null(fk in true_ids)
    
    @property
    def heating_supply(self):
        if not self._heating_supply:
            PERSONAL_GAS = 1
            PERSONAL_TD = 2
            PERSONAL_ELECTRIC = 3
            CENTRAL = 4  
            NO = 8      
            true_ids = (PERSONAL_GAS,PERSONAL_TD,PERSONAL_ELECTRIC,CENTRAL)                    
            if self._basic_bidg:                
                self._heating_supply = self._supply(true_ids, NO, self._basic_bidg.heating_id)
        return self._heating_supply
    
    @property
    def water_supply(self):
        if not self._water_supply:
            VODOPROVOD = 1
            PODKLUCHENO = 7
            NO = 10 
            true_ids = (VODOPROVOD,PODKLUCHENO)
            self._water_supply = self._supply(true_ids, NO, self._estate.watersupply_id)
        return self._water_supply

    @property
    def sewerage_supply(self):
        if not self._sewerage_supply:
            PODKLUCHENO = 5
            CENTRAL = 8
            NO = 9
            true_ids = (CENTRAL,PODKLUCHENO)
            self._sewerage_supply = self._supply(true_ids, NO, self._estate.sewerage_id)
        return self._sewerage_supply
    
    @property
    def electricity_supply(self):
        if not self._electricity_supply:
            PODKLUCHENO = 5
            NO = 7
            true_ids = (PODKLUCHENO,)             
            self._electricity_supply = self._supply(true_ids, NO, self._estate.electricity_id)
        return self._electricity_supply
    
    @property
    def gas_supply(self):
        if not self._gas_supply:
            PODKLUCHENO = 5
            NO = 7
            true_ids = (PODKLUCHENO,)             
            self._gas_supply = self._supply(true_ids, NO, self._estate.gassupply_id)
        return self._gas_supply
        
    @property
    def balcony(self):
        if not self._balcony:     
            balcons_node = None
            loggias_node = None
            result = []        
            if self._basic_bidg:
                balcons_count = self._basic_bidg.get_balcons_count()            
                if balcons_count == 1:
                    balcons_node = u'балкон'
                elif 1 < balcons_count < 5:
                    balcons_node = u'%s балкона' % balcons_count
                elif  balcons_count > 5:
                    balcons_node = u'%s балконов' % balcons_count            
                if balcons_node:
                    result.append(balcons_node)            
                loggias_count = self._basic_bidg.get_loggias_count()
                if loggias_count == 1:
                    loggias_node = u'лоджия'
                elif 1 < loggias_count < 5:
                    loggias_node = u'%s лоджии' % balcons_count
                elif  loggias_count > 5:
                    loggias_node = u'%s лоджий' % balcons_count            
                if loggias_node:
                    result.append(loggias_node)            
                if result:
                    self._balcony = u', '.join(result)          
        return self._balcony
    
    @property
    def bathroom_unit(self):
        if not self._bathroom_unit:
            result = []
            if self._basic_bidg:
                sovmest_count = self._basic_bidg.get_sanuzel_sovmest_count()
                if sovmest_count == 1:
                    result.append(u'совмещенный')
                if sovmest_count > 1:
                    result.append(u'%s совмещенных' % sovmest_count)                
                razdel_count = self._basic_bidg.get_sanuzel_razdel_count()                
                if razdel_count == 1:
                    result.append(u'раздельный')
                if razdel_count > 1:
                    result.append(u'%s раздельных' % razdel_count)
                if result:
                    self._bathroom_unit = u', '.join(result)
        return self._bathroom_unit
    
    @property                
    def floor_covering(self):
        if not self._floor_covering:
            if self._basic_bidg and self._basic_bidg.flooring:
                self._floor_covering = u'%s' % self._basic_bidg.flooring
                self._floor_covering.lower() 
        return self._floor_covering
             
    @property           
    def window_view(self):
        if not self._window_view:
            try:
                beside = self._estate.entrances.get(entranceestate__type=EntranceEstate.WINDOWVIEW, entranceestate__basic=True)
                self._window_view = u'%s' % beside.name                
            except:
                pass                
        return self._window_view

    def get_yandex_building(self):
        if not self._yandex_building:
            if self.new_flat and self._basic_bidg:
                self._yandex_building = self._basic_bidg.yandex_building
        return self._yandex_building
    
    @property
    def building_name(self):
        if not self._building_name:
            if self.new_flat:
                yandex_building = self.get_yandex_building()                                
                self._building_name = u'%s' % yandex_building.name if yandex_building else u'%s' % self.address.sub_locality 
        return self._building_name
        
    @property
    def yandex_building_id(self):
        if not self._yandex_building_id:
            if self.new_flat:
                yandex_building = self.get_yandex_building()
                if yandex_building:
                    self._yandex_building_id = u'%s' % yandex_building.building_id                              
        return self._yandex_building_id
    
    @property    
    def building_type(self):
        if not self._building_type:
            if self._basic_bidg: 
                # TODO: admin WallConstrucion               
                self._building_type = self.get_value_mapper(WallConstrucion, self._basic_bidg.wall_construcion_id, 'BuildingType')
        return self._building_type
    
    @property    
    def built_year(self):
        if not self._built_year:
            if self._basic_bidg:
                self._built_year = number2xml(self._basic_bidg.year_built)    
        return self._built_year
             
    @property  
    def ready_quarter(self):
        if not self._ready_quarter:
            if self._new_flat:
                yandex_building = self.get_yandex_building()
                if yandex_building:                    
                    self._ready_quarter = number2xml(yandex_building.ready_quarter)
        return self._ready_quarter   
                    
    @property    
    def building_state(self):
        if not self._building_state:
            if self._new_flat:
                yandex_building = self.get_yandex_building()
                if yandex_building:
                    self._building_state = u'%s' % yandex_building.building_state
        return self._building_state
    
    @property
    def lift(self):
        if not self._lift:
            if self._basic_bidg and self._basic_bidg.elevator:
                self._lift = self.bool_to_xml(True)
        return self._lift
    
    @property
    def ceiling_height(self):
        if not self._ceiling_height:        
            if self._basic_bidg:
                self._ceiling_height = number2xml(self._basic_bidg.ceiling_height)
        return self._ceiling_height
    
    @property
    def object_type(self):
        if not self._object_type:                                     
            if self._estate_type_id:                
                self._object_type = self.get_value_mapper(EstateType, self._estate_type_id, 'ObjectType')
                if not self._object_type:
                    name = u'%s' % self._basic_bidg.estate_type.name.lower()
                    self._object_type = name                     
        return self._object_type    
        