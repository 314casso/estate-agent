# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from realty.utils import join_strings

class RealtyItem(Item):
    do_not_process = Field()
    BIDG_FIELDS = ('room_count', )
    phone = Field()    
    desc = Field()
    name = Field()
    price = Field()
    price_digit = Field()
    link = Field()
    estate_type_id = Field() 
    region_id = Field()
    locality_id = Field()
    microdistrict = Field()
    street = Field()
    estate_number = Field()
    room_count = Field()
    phone_filename = Field()
        
    def has_extra_bidg(self):        
        for field in self.BIDG_FIELDS:
            if self[field]:
                return True  
        
    def print_item(self):        
        print '********* ITEM *********'
        for key, value in self._values.iteritems():
            txt = ''
            if type(value) is list:
                for v in value:
                    txt += u'%s ' % v                                     
            else:
                txt = '%s' % value            
            print "KEY [ %s: %s ]" % (key, txt)
        print '********* END *********'
            
    
        

