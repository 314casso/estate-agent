# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class RealtyItem(Item):
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
        
    def has_extra_bidg(self):        
        for field in self.BIDG_FIELDS:
            if self[field]:
                return True  
        


